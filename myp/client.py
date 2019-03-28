# -*- coding: utf-8 -*-

from socket import *
import sys
from time import ctime

HOST = 'localhost'
PORT = 10000
BUFSIZE = 1024
ADDR = (HOST, PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    clientSocket.connect(ADDR)
    clientSocket.send('Hello!'.encode())

except Exception as e:
    print('%s:%s' % ADDR)
    sys.exit()

print('connect is success')
