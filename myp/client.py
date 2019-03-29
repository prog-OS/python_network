# -*- coding: utf-8 -*-
import socket
from threading import Thread

HOST = 'localhost'
PORT = 9010

def rcvMsg(sock, username):
	while True:
		try:
			data = sock.recv(1024)
			if not data:
				break
			print(data.decode() + ('\n[%s] ' % username), end='')
			# print(data.decode())
			# print('[rcv][%s] ' % username).strip() # 위에 실행뒤 이게 안나옴...
		except:
			pass

def runChat():
	name = False

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.connect((HOST, PORT))
			
		data = sock.recv(1024)
		print(data.decode(), end='') # 로그인 ID : 

		while True:
			msg = input()
			if name == False:
				username = msg.strip()
				name = True
				thr = Thread(target=rcvMsg, args=(sock, username))
				thr.daemon = True
				thr.start()
				
			if msg == '/quit':
				sock.send(msg.encode())
				thr.daemon = False
				break

			print('[%s] ' % username, end='')
			sock.send(msg.encode())

runChat()