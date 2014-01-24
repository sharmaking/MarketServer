#!/usr/bin/python
# -*- coding: utf-8 -*-
# winController.py
from PyQt4 import QtCore
import datetime

class QWindowsController(QtCore.QThread):
	def __init__(self, mainController):
		QtCore.QThread.__init__(self)
		self.mainController = mainController
		self.QMain = mainController.QMain
		self.preWatchTime = datetime.datetime(1990,1,1,0,0,0)

	def __del__(self):
		self.wait()

	def run(self):
		while True:
			self.showMarketTime()
			self.showLocalTime()
			self.watchLinkOutOffLine()
		self.terminate()
	#显示行情时间
	def showMarketTime(self):
		marketTime = self.mainController.strategyServer.dataServerInstance.currentMarketDateTime
		marketTimeStr = marketTime.strftime("%H:%M:%S")
		self.QMain.showMarketTime(marketTimeStr)
	#显示本机时间
	def showLocalTime(self):
		localTime = datetime.datetime.now()
		localTimeStr = localTime.strftime("%H:%M:%S")
		self.QMain.showLocalTime(localTimeStr)
	#监视链接断线
	def watchLinkOutOffLine(self):
		nowTime = datetime.datetime.now()
		if (nowTime - self.preWatchTime).seconds > 10:
			for macAddress, linkObj in self.mainController.linkObjDict.items():
				try:
					linkObj["RequesHandler"].request.sendall("T")
				except Exception:
					self.mainController.linkOffLine(macAddress)		
			self.preWatchTime = nowTime
