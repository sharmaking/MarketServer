#!/usr/bin/python
# -*- coding: utf-8 -*-
# mainWindow.py
from PyQt4 import QtGui, QtCore, uic

class QMainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(QMainWindow,self).__init__()
		self.initUI()

	#初始化窗口布局
	def initUI(self):
		uic.loadUi('ui/mainWindow.ui', self)
		self.setWindowTitle(u'信号客户端')
		self.statusBar().showMessage(u'正在连接服务器')	
