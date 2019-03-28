from socket import *

HOST = ''
PORT = 10000
BUFSIZE = 1024
ADDR = (HOST, PORT)

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(ADDR)
print('bind')

serverSocket.listen(100)
print('listen')

def menu(clientSocket):
    clientSocket.send('--- 채팅 서버 시작 ---\n'.encode())
    clientSocket.send('--- 환영합니다 ---'.encode())

try:
    while True:
    
        clientSocket, addr_info = serverSocket.accept()
        print('accept')
        print('--client information--')
        print(clientSocket)
        print('----------------------')

        clientSocket.send('test'.encode())
        menu(clientSocket)
        # data = clientSocket.recv(65535)
        # print('recieve data : ', data.decode())

        # -------------------------------------
        # conn.send


        # -------------------------------------
except KeyboardInterrupt:
    clientSocket.close()
    serverSocket.close()
    print('close')
