# -*- coding: utf-8 -*-
import socket
from threading import Thread

HOST = 'localhost'
PORT = 9009

def runChat():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.connect((HOST, PORT))

		while True:
			msg = input()
			if msg == '/quit':
				sock.send(msg.encode())
				break
			sock.send(msg.encode())

runChat()