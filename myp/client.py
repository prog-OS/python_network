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

			print(data.decode() + ('\n[%s] ' % username), end='') # 내용 출력후 자신의 아이디 출력

			# print(data.decode())
			# print('[rcv][%s] ' % username, end='')
			# print('', end='')
			
			# print(data.decode())
			# print('[rcv][%s] ' % username, end='') # 위에 실행뒤 이게 안나옴...
		except:
			pass


def runChat():

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.connect((HOST, PORT))

		data = sock.recv(1024) # 로그인 ID :	
		print(data.decode(), end='') # 로그인 ID : 출력

		username = input()
		sock.send(username.encode())

		while True:	
			data = sock.recv(1024) # permission or 이미 등록
			
			if data.decode() != "permission":
				print(data.decode(), end='') # 이미 등록 
				data = sock.recv(1024) # 로그인 ID
				print(data.decode(), end='') # 출력
				
				username = input()
				sock.send(username.encode())
			else:
				break

		t = Thread(target=rcvMsg, args=(sock, username))
		t.daemon = True
		t.start()

		while True:
			print('[%s] ' % username, end='')
			msg = input()			
			if msg.find('/quit') != -1:
				msg = '/quit'
				sock.send(msg.encode())
				break
			sock.send(msg.encode())
			

runChat()