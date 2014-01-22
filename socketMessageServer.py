#!/usr/bin/python
# -*- coding: utf-8 -*-
#socketMessageServer.py
import SocketServer
import threading
import struct

class NoticeRequesHandler(SocketServer.BaseRequestHandler):
	def setup(self):
		self.mainController = self.server.mainController
	def handle(self):
		print '...connected from:', self.client_address
		self.recvSubscibeRespond()
	#--------------------
	#监听socket缓存
	def recvSubscibeRespond(self):
		bufferData = ""
		while 1:
			recvData = self.request.recv(1024)
			#如果缓冲没有数据
			if not bufferData:
				bufferData = recvData
			else: #继续缓冲数据
				bufferData = bufferData + recvData
			#接收数据完整，处理缓冲数据
			if self.checkBufferDataIsComplete(bufferData):
				bufferData = self.handleBufferData(bufferData)
	#判断数据是否接收完整
	def checkBufferDataIsComplete(self, bufferData):
		if len(bufferData)>8:
			length = struct.unpack("i", bufferData[4:8])[0]
			if len(bufferData) >= (length + 8):
				return True
		return False
	#处理接收数据
	def handleBufferData(self, bufferData):
		tempBufferData = bufferData
		#如果缓存区为空直接返回
		while self.checkBufferDataIsComplete(tempBufferData):
			dataType = struct.unpack("i", tempBufferData[:4])[0]
			length = struct.unpack("i", tempBufferData[4:8])[0]
			completBufferDate = tempBufferData[:length+8]
			self.resolveRecvData(completBufferDate)
			tempBufferData = tempBufferData[length+8:]
			if len(tempBufferData) < 8:
				break
			pass
		return tempBufferData
	#解析接收的数据类型调用相应的方法
	def resolveRecvData(self, bufferData):
		dataType = struct.unpack("i", bufferData[:4])[0]
		length = struct.unpack("i", bufferData[4:8])[0]
		if dataType == 0:
			self.fomartRegisterPara(bufferData[8:])
	def fomartRegisterPara(self, registerPara):
		linkPara = eval(registerPara)
		linkPara["IPAddress"] = self.client_address
		linkPara["RequesHandler"] = self
		self.mainController.registerLink(linkPara)

class CSocketMessageServer(threading.Thread):
	def __init__(self, Host, Port, mainController):
		super(CSocketMessageServer, self).__init__()
		self.name = "SocketMessageServer-Thread"
		self.mainController = mainController
		self.threadingTCPServer = SocketServer.ThreadingTCPServer((Host, Port), NoticeRequesHandler)
		self.threadingTCPServer.mainController = mainController

	def run(self):
		print self.threadingTCPServer
		print 'waiting for connection...'
		self.threadingTCPServer.serve_forever()
