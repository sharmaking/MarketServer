#!/usr/bin/python
# -*- coding: utf-8 -*-
HOST   = 'localhost' 
PORT   = 21567 
BUFSIZ = 1024
ADDR   = (HOST, PORT)

import socket
import struct
import uuid

def subscibeMacAddress(socketLink, registerPara):
	fmt = "ii%ds" %len(registerPara)
	sn = 0
	length = len(registerPara)
	bytes = struct.pack(fmt, sn, length, registerPara)
	print sn, length, len(bytes), bytes
	socketLink.send(bytes)

def test():
	pass

def main():
	test()

	tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpClient.connect(ADDR)

	macAddress = uuid.UUID(int = uuid.getnode()).hex[-12:]
	
	registerPara = {
		"macAddress"	: macAddress,
		"subStocks"		: ["999999", "300238"],
		"subSignals"	: ["SQTSignal"],
		"subMultiples"	: []
	}	

	subscibeMacAddress(tcpClient, str(registerPara))

	pass

if __name__ == '__main__':
	main()