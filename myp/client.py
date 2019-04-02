# -*- coding: utf-8 -*-
import socket
from threading import Thread

HOST = 'localhost'
PORT = 9010

name = False
unPermission = False

def rcvMsg(sock, username):
	global unPermission

	while True:
		try:
			data = sock.recv(1024)
			if not data:
				break
			print(data.decode())
			if unPermission == False and data.decode() == "permission":
				print("unPermission = True")
				name = True
				unPermission = True
			elif unPermission == False and data.decode() != "permission":
				print('zzz')
				continue
			print('end if')
			print(data.decode() + ('\n[%s] ' % username), end='') # 내용 출력후 자신의 아이디 출력

			# print(data.decode())
			# print('[rcv][%s] ' % username, end='')
			# print('', end='')
			
			# print(data.decode())
			# print('[rcv][%s] ' % username, end='') # 위에 실행뒤 이게 안나옴...
		except:
			pass

def runChat():
	global name
	global unPermission

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.connect((HOST, PORT))
			
		data = sock.recv(1024)
		print(data.decode(), end='') # 로그인 ID : 출력

		while True:
			msg = input()
			sock.send(msg.encode())
			if name == True:
				username = msg.strip()
				thr = Thread(target=rcvMsg, args=(sock, username))
				thr.daemon = True
				thr.start()
				
			if msg == '/quit':
				sock.send(msg.encode())
				# thr.daemon = False
				break

			if unPermission == True:
				print('[%s] ' % username, end='')
			

runChat()