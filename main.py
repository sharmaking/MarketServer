#!/usr/bin/python
# -*- coding: utf-8 -*-
import dataServerContoller
import mainWindow

def main():
	mainController = dataServerContoller.CDataServerContoller()
	#窗口显示
	mainWindow.main(mainController)
	pass

if __name__ == '__main__':
	main()