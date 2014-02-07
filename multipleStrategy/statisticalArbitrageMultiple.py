#!/usr/bin/python
# -*- coding: utf-8 -*-
#statisticalArbitrageMultiple.py
import baseMultiple
import numpy

class CStatisticalArbitrageMultiple(baseMultiple.CBaseMultiple):
	#------------------------------
	#继承重载函数
	#------------------------------
	#自定义初始化函数
	def customInit(self):
		self.name = "statisticalArbitrageMultiple"
		self.parameters = []
		self.parameters.append({
			"stocks"	: ["600000", "601169"],
			"Beta"		: 0.98691,
			"Mean"		: 0.26554,
			"STD"		: 0.015365,
			"OPEN"		: 1.6,
			"CLOSE"		: 0.06,
			"ODD"		: 2.5,
			"staute"	: 0,
			"tradeType"	: [None, None],
			"price"		: [0,0],
			"S"			: []
			})
		self.parameters.append({
			"stocks"	: ["600648", "600663"],
			"Beta"		: 1.26784,
			"Mean"		: -0.08965,
			"STD"		: 0.038629,
			"OPEN"		: 1.1,
			"CLOSE"		: 0.06,
			"ODD"		: 2.5,
			"staute"	: 0,
			"tradeType"	: [None, None],
			"price"		: [0,0],
			"S"			: []
			})

	#行情数据触发函数
	def onRtnMarketData(self, data):
		#计算S
		self.countS(data)
		pass
	def dayBegin(self):
		pass
	def dayEnd(self):
		pass
	#自动保存缓存触发函数
	def autosaveCache(self):
		#self.saveCache(data = self.data)
		pass
	#----------------------
	#实现函数体
	#----------------------
	def countS(self, data):
		for parameter in self.parameters:
			Pa = self.getStockPrice(parameter["stocks"][0])
			Pb = self.getStockPrice(parameter["stocks"][1])
			if Pa and Pb:
				St = numpy.log(Pa) - parameter["Beta"]*numpy.log(Pb)
				S = (St - parameter["Mean"])/parameter["STD"]
				parameter["S"].append((data["dateTime"], S))
				self.sendS(S, parameter["stocks"][0])
				self.countTrade(parameter, S)
				parameter["price"] = [Pa, Pb]
	def getStockPrice(self, stockCode):
		if self.controller.listenerDict[stockCode].signalObjDict["baseSignal"].MDList:
			return self.controller.listenerDict[stockCode].signalObjDict["baseSignal"].MDList[-1]["close"]
		return None
	def countTrade(self, parameter, S):
		if parameter["staute"] == 0:	#还没开仓
			if S > parameter["OPEN"]:
				self.openTrade(parameter, True)		#正
			elif S < -parameter["OPEN"]:
				self.openTrade(parameter, False)	#反
		elif parameter["staute"] == 1:
			if parameter["tradeType"][0] == "Sell":	#正
				if S < parameter["CLOSE"]:	#平
					self.closeTrade(parameter)
				if S > parameter["ODD"]:	#止损
					self.stopLossTrade(parameter)
			elif parameter["tradeType"][0] == "Buy":	#反
				if S > -parameter["CLOSE"]:	#平
					self.closeTrade(parameter)
				if S < -parameter["ODD"]:	#止损
					self.stopLossTrade(parameter)
		if S > parameter["ODD"] or S < -parameter["ODD"]:
			pass
	def sendS(self, S, stockCode):
		self.sendMessageToClient(u"0_%s_%s"%(stockCode, str(S)[:6]))
	def openTrade(self, parameter, isTrue):
		parameter["staute"] = 1
		if isTrue:		#正
			parameter["tradeType"] = ["Sell", "Buy"]
		else:			#反
			parameter["tradeType"] = ["Buy", "Sell"]
		self.sendMessageToClient(u"1_%s_开仓：%s %s %s, %s %s %s"%(
			parameter["stocks"][0],
			parameter["stocks"][0], parameter["tradeType"][0],parameter["price"][0],
			parameter["stocks"][1], parameter["tradeType"][1],parameter["price"][1]))
		print u"开仓：%s %s %s, %s %s %s"%(
			parameter["stocks"][0], parameter["tradeType"][0],parameter["price"][0],
			parameter["stocks"][1], parameter["tradeType"][1],parameter["price"][1])
	def closeTrade(self, parameter):
		self.sendMessageToClient(u"1_%s_平仓：%s %s %s, %s %s %s"%(
			parameter["stocks"][0],
			parameter["stocks"][0], parameter["tradeType"][1],parameter["price"][0],
			parameter["stocks"][1], parameter["tradeType"][0],parameter["price"][1]))
		parameter["staute"]		= 0
		parameter["tradeType"]	= [None, None]
	def stopLossTrade(self, parameter):
		self.sendMessageToClient(u"1_%s_止损：%s %s %s, %s %s %s"%(
			parameter["stocks"][0],
			parameter["stocks"][0], parameter["tradeType"][1],parameter["price"][0],
			parameter["stocks"][1], parameter["tradeType"][0],parameter["price"][1]))
		parameter["staute"]		= 0
		parameter["tradeType"]	= [None, None]
	def exceptionTrade(self, parameter):
		self.sendMessageToClient(u"1_%s_异常：%s %s %s, %s %s %s"%(
			parameter["stocks"][0],
			parameter["stocks"][0], parameter["tradeType"][1],parameter["price"][0],
			parameter["stocks"][1], parameter["tradeType"][0],parameter["price"][1]))
		parameter["staute"]		= 0
		parameter["tradeType"]	= [None, None]
