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
except Exception as e:
    print('%s:%s' % ADDR)
    sys.exit()



data = clientSocket.recv(BUFSIZE)
print('%s\n' % data.decode())
data = clientSocket.recv(BUFSIZE)
print('%s\n' % data.decode())

