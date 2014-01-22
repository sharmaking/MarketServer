#!/usr/bin/python
# -*- coding: utf-8 -*-
#mainController.py
import socketMessageServer
import dataServer
import datetime

class CMainController(object):
	def __init__(self):
		super(CMainController, self).__init__()
		#连接对象池
		self.linkObjDict = {}
		#读取设置参数
		execfile("config.ini")
		#启动信号服务器
		self.messageServer = socketMessageServer.CSocketMessageServer(
				self.MessageServer_HOST,
				self.MessageServer_PORT,
				self
			)
		self.messageServer.start()
		#启动数据服务器
		self.strategyServer = dataServer.CDataServer(
				self.DataServer_HOST,
				self.DataServer_PORT,
				self.REQUEST_TYPE,		#0：请求当天数据，1：请求某一天数据，2：请求某一段时间数据
				self.REQUEST_FLAG,		#0：实时请求，1：从开盘时间重新接收，2：按指定时间开始接收(仅在REQUEST_TYPE=0时有意义)
				self.START_TIME, 		#请求数据开始时间
				self.END_TIME,			#请求数据结束时间
				self.SUB_ALL_STOCK,
				self
			)
		self.strategyServer.creatDataServerLink()	#创建数据连接

	#注册信号客户端连接
	def registerLink(self, linkPara):
		self.linkObjDict[linkPara["macAddress"]] =linkPara
		self.strategyServer.initLink(linkPara)

		self.strategyServer.dataServerInstance.requestData(
			self.REQUEST_TYPE,
			self.REQUEST_FLAG,
			datetime.datetime.strptime(self.START_TIME,"%Y-%m-%d %H:%M:%S"),
			datetime.datetime.strptime(self.END_TIME,"%Y-%m-%d %H:%M:%S"))


def main():
	test = CMainController()

if __name__ == '__main__':
	main()