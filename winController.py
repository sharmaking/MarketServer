#!/usr/bin/python
# -*- coding: utf-8 -*-
# winController.py
from PyQt4 import QtCore

class QWindowsController(QtCore.QThread):
	def __init__(self, mainController):
		QtCore.QThread.__init__(self)
		self.mainController = mainController
		self.QMain = mainController.QMain

	def __del__(self):
		self.wait()

	def run(self):
		while True:
			pass
		self.terminate()