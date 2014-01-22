#!/usr/bin/python
# -*- coding: utf-8 -*-
#controller.py
import copy
import time
import datetime
#自定义类
import dataServerApi
import dataListener
#载入策略
import signalStrategy
import multipleStrategy

class CDataServer(object):
	def __init__(self, DataServer_HOST,	DataServer_PORT, REQUEST_TYPE, REQUEST_FLAG, START_TIME, END_TIME, SUB_ALL_STOCK, mainController):
		super(CDataServer, self).__init__()
		self.DataServer_HOST	= DataServer_HOST	#数据服务器IP地址
		self.DataServer_PORT	= DataServer_PORT	#数据服务器端口号
		self.REQUEST_TYPE 		= REQUEST_TYPE		#0：请求当天数据，1：请求某一天数据，2：请求某一段时间数据
		self.REQUEST_FLAG		= REQUEST_FLAG		#0：实时请求，1：从开盘时间重新接收，2：按指定时间开始接收(仅在REQUEST_TYPE=0时有意义)
		self.START_TIME 	 	= START_TIME 		#请求数据开始时间
		self.END_TIME			= END_TIME			#请求数据结束时间
		self.SUB_ALL_STOCK		= SUB_ALL_STOCK		#是否定义全部股票
		self.mainController	= mainController
		#-----------------------
		#定义全局变量
		#-----------------------
		#数据监听对象
		self.listenerDict = {}		#每个合约一个个对象
		#策略对象列表
		self.strategyDict = {}		#key: 策略名，value：策略对象
		#订阅股票列表
		self.subStocks = []
		#数据缓存堆栈
		self.bufferStack = {}		#key: stockCode, value: list
		#信号槽
		self.messageBox = []
		#-----------------------
	#-----------------------
	#实现函数
	#-----------------------
	#创建数据连接对象
	def creatDataServerLink(self):
		self.dataServerInstance = dataServerApi.CDataServerApi(self.DataServer_HOST,self.DataServer_PORT)
		self.dataServerInstance.init(self)
		self.dataServerInstance.connectServer()
		self.dataServerInstance.requestData(
			self.REQUEST_TYPE,
			self.REQUEST_FLAG,
			datetime.datetime.strptime(self.START_TIME,"%Y-%m-%d %H:%M:%S"),
			datetime.datetime.strptime(self.END_TIME,"%Y-%m-%d %H:%M:%S"))
	#-----------------------
	#链接触发
	#链接初始化
	def initLink(self, linkPara):
		self.subStocks.extend(linkPara["subStocks"])
		self.creatListenerWhileBeConnected(linkPara)
		self.dataServerInstance.initMainIFSubStock()
		#订阅股票
		self.dataServerInstance.subscibeStock(self.SUB_ALL_STOCK, self.subStocks)
	def creatListenerWhileBeConnected(self, linkPara):
		for stock in linkPara["subStocks"]:
			if not self.listenerDict.has_key(stock):
				strategyObjDict = self.creatStrategyObjectWhileBeConnected(True, stock, linkPara)
				if strategyObjDict:
					self.bufferStack[stock]		= []
					newListener           		= dataListener.CDataListener(stock, self.bufferStack)
					newListener.setDaemon(True)
					newListener.getSignalStrategyObj(strategyObjDict)
					newListener.getLinkPara(linkPara)
					newListener.start()
					self.listenerDict[stock]	= newListener
			else:
				strategyObjDict = self.creatStrategyObjectWhileBeConnected(True, stock, linkPara)
				if strategyObjDict:
					self.listenerDict[stock].getSignalStrategyObj(strategyObjDict)
					self.listenerDict[stock].getLinkPara(linkPara)
		if not self.listenerDict.has_key("Multiple"):
			strategyObjDict = self.creatStrategyObjectWhileBeConnected(False,"Multiple", linkPara)
			if strategyObjDict:
				self.bufferStack["Multiple"]	= []
				newListener						= dataListener.CDataListener("Multiple", self.bufferStack)
				newListener.setDaemon(True)
				newListener.getmultipleStrategyObj(strategyObjDict, self.listenerDict)
				newListener.getLinkPara(linkPara)
				newListener.start()
				self.listenerDict["Multiple"]	= newListener
			else:
				strategyObjDict = self.creatStrategyObjectWhileBeConnected(False, stock, linkPara)
				if strategyObjDict:
					self.listenerDict[stock].getSignalStrategyObj(strategyObjDict)
					self.listenerDict[stock].getLinkPara(linkPara)
	def creatStrategyObjectWhileBeConnected(self, needSignal, stock, linkPara):
		strategyObjDict = {}
		if needSignal:	#单合约策略
			if not linkPara["subSignals"]:		#如果没有订阅
				return False
			for signalName in linkPara["subSignals"]:
				singalObjStr = "signalStrategy.C%s%s()" %(signalName[0].upper(),signalName[1:])
				strategyObjDict[signalName] = eval(singalObjStr)
				strategyObjDict[signalName].init(stock, self)
			return strategyObjDict
		else:			#多合约策略
			if not linkPara["subMultiples"]:	#如果没有订阅
				return False
			for multipeName in linkPara["subMultiples"]:
				multipeObjStr = "multipleStrategy.C%s%s()" %(multipeName[0].upper(),multipeName[1:])
				strategyObjDict[multipeName] = eval(multipeObjStr)
				strategyObjDict[multipeName].init("Multiple", self)
			return strategyObjDict
	#--------------------
	#更新主力合约
	def updateMainIF(self, mainIF):
		self.subStocks.append(mainIF)
		
		subSignalList		= []
		subMultiplesList	= []
		linkObjs			= []

		for macAddress, linkPara in self.mainController.linkObjDict.items():
			if "IF0000" in linkPara["subStocks"]:
				subSignalList.extend(linkPara["subSignals"])
				subMultiplesList.extend(linkPara["subMultiples"])
				linkObjs.append(linkPara)
		subSignalList		= list(set(subSignalList))
		subMultiplesList	= list(set(subMultiplesList))

		strategyObjDict = {}
		if subSignalList:
			for signalName in linkPara["subSignals"]:
				singalObjStr = "signalStrategy.C%s%s()" %(signalName[0].upper(),signalName[1:])
				strategyObjDict[signalName] = eval(singalObjStr)
				strategyObjDict[signalName].init(mainIF, self)
		
		self.bufferStack[mainIF]		= []
		newListener           		= dataListener.CDataListener(mainIF, self.bufferStack)
		newListener.setDaemon(True)
		newListener.getSignalStrategyObj(strategyObjDict)
		newListener.getLinkPara(linkPara)
		newListener.start()
		self.listenerDict[mainIF]	= newListener
		#订阅股票
		self.dataServerInstance.subscibeStock(self.SUB_ALL_STOCK, self.subStocks)
