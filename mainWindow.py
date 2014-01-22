#!/usr/bin/python
# -*- coding: utf-8 -*-
# mainWindow.py
import sys
from PyQt4 import QtGui, QtCore, uic
import copy
import datetime

class QMainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(QMainWindow,self).__init__()
		self.initUI()

	#初始化窗口布局
	def initUI(self):
		uic.loadUi('ui/mainWindow.ui', self)
		self.setWindowTitle(u'信号客户端')
		self.statusBar().showMessage(u'正在连接服务器')	

#信号监听器
class QListener(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)

	def __del__(self):
		self.wait()

	def run(self):
		while True:
			pass
		self.terminate()

def main(controller):
	app = QtGui.QApplication(sys.argv)
	Qmain = QMainWindow()
	#创建信号监视进程
	messageListener = QListener()
	messageListener.start()
	#显示主窗口
	Qmain.show()
	sys.exit(app.exec_())
 	pass