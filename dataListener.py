#!/usr/bin/python
# -*- coding: utf-8 -*-
#dataListener.py
import threading

class CDataListener(threading.Thread):
	def __init__(self, name, bufferStack):
		super(CDataListener, self).__init__()
		self.stockCode = name
		self.name = "Thread-%s-Listener" %name
		self.bufferStack = bufferStack
		#连接对象
		self.linkParaDict = {}
		#策略对象
		self.type = True     		#监听类型： True 单股票策略监听，False 多股票策略监听
		self.listenerDict = {}
		self.signalObjDict = {}		#单股票策略对象列表
		self.multipleObjDict = {}	#多合约策略对象列表
	#----------------------------
	#获得连接对象
	#----------------------------
	def getLinkPara(self, linkPara):
		self.linkParaDict[linkPara["macAddress"]] = linkPara
	#----------------------------
	#获得策略对象
	#----------------------------
	#单股票策略
	def getSignalStrategyObj(self, signalObjDict):
		for signalName, signalObj in signalObjDict.items():
			if not self.signalObjDict.has_key(signalName):
				self.signalObjDict[signalName] = signalObj
		self.type = True
	#多股票策略
	def getmultipleStrategyObj(self, multipleObjDict, listenerDict):
		for multipleName, multipleObj in multipleObjDict.items():
			if not self.multipleObjDict.has_key(multipleName):
				self.multipleObjDict[multipleName] = multipleObj
		self.listenerDict = listenerDict
		self.type = False
	#----------------------------
	#主函数，监听数据更新
	#----------------------------
	def run(self):
		while 1:
			while self.bufferStack[self.stockCode]:
				dataType, data = self.bufferStack[self.stockCode][0]
				del self.bufferStack[self.stockCode][0]
				self.dataListening(dataType, data)
	def dataListening(self, dataType, data):
		if self.type:
			for signalName, signalObj in self.signalObjDict.items():
				signalObj.dataListener(dataType, data)
		else:
			for multipleName, multipleObj in self.multipleObjDict.items():
				multipleObj.dataListener(dataType, data)
