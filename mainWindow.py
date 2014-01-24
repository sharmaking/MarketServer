#!/usr/bin/python
# -*- coding: utf-8 -*-
# mainWindow.py
from PyQt4 import QtGui, QtCore, uic
import datetime

class QMainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(QMainWindow,self).__init__()
		self.initUI()
		self.initEventConnection()
		self.linkObjDict = {}
	#初始化窗口布局
	def initUI(self):
		uic.loadUi('ui/mainWindow.ui', self)
		self.setWindowTitle(u'信号客户端')
		self.statusBar().showMessage(u'正在连接服务器')
	def initEventConnection(self):
		self.link_listWidget.itemDoubleClicked.connect(self.showSubStrategyByClick)
	#切换选择链接订阅策略
	def showSubStrategyByClick(self):
		currentItem = self.link_listWidget.currentItem()
		macAddress = currentItem.text().split("-")[1]
		self.showSubStrategy(unicode(macAddress))
	#显示行情时间
	def showMarketTime(self, marketTime):
		self.marketTime_LCD.display(marketTime)
	#显示本地时间
	def showLocalTime(self, localTime):
		self.localTime_LCD.display(localTime)
	#添加日志日志
	def addLog(self, logStr):
		self.log_listWidget.addItem(logStr)
		if self.log_listWidget.count() > 100:
			self.log_listWidget.takeItem(0)
		self.saveLog(logStr)
	#保存日志
	def saveLog(self, logStr):
		logFile = open("log.log", "a")
		content = "%s %s\n"%(str(datetime.datetime.now()), logStr.encode('gb2312'))
		logFile.write(content)
		logFile.close()
	#显示连接接入
	def showMessageClientJoinUp(self, linkPara):
		if not self.linkObjDict.has_key(linkPara["macAddress"]):
			self.linkObjDict[linkPara["macAddress"]] =linkPara
			messageItem = QtGui.QListWidgetItem("%s-%s"%(linkPara["IPAddress"][0], linkPara["macAddress"]))
			self.link_listWidget.addItem(messageItem)
			self.showSubStrategy(linkPara["macAddress"])
		self.linkObjDict[linkPara["macAddress"]] =linkPara
		self.addLog(u"%s 信号客户端连入服务器"%linkPara["IPAddress"][0])
	#显示订阅策略
	def showSubStrategy(self, macAddress):
		while self.strategy_listWidget.count():
			self.strategy_listWidget.takeItem(0)
		for x in self.linkObjDict[macAddress]["subSignals"]:
			self.strategy_listWidget.addItem(x)
		for x in self.linkObjDict[macAddress]["subMultiples"]:
			self.strategy_listWidget.addItem(x)