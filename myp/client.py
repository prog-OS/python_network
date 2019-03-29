# -*- coding: utf-8 -*-
import socket
from threading import Thread

HOST = 'localhost'
PORT = 9010

def rcvMsg(sock):
	while True:
		try:
			data = sock.recv(1024)
			if not data:
				break
			print(data.decode())
		except:
			pass

def runChat():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.connect((HOST, PORT))
		thr = Thread(target=rcvMsg, args=(sock,))
		thr.daemon = True
		thr.start()

		while True:
			msg = input()
			if msg == '/quit':
				sock.send(msg.encode())
				break
			sock.send(msg.encode())

runChat()