# -*- coding: utf8 -*-

from socket import *
from select import *
import sys
from time import ctime

# host, port, buffer size
HOST = ''
PORT = 9009
BUFSIZE = 1024
ADDR = (HOST, PORT)

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(ADDR)

serverSocket.listen(10)
connection_list = [serverSocket]
print('================================================')
print('채팅 서버를 시작합니다. %s 포트로 접속을 기다립니다.' % str(PORT))
print('================================================')

while connection_list:
    try:
        print('[INFO] 요청을 기다립니다...')

        # select 로 요청을 받고, 10초마다 블럭킹을 해제하도록 함
        read_socket, write_socket, error_socket = select(connection_list, [], [], 10)

        for sock in read_socket:
            # 새로운 접속
            if sock == serverSocket:
                clientSocket, addr_info = serverSocket.accept()
                connection_list.append(clientSocket)
                print('[INFO][%s] client(%s)가 새롭게 연결 되었습니다.' % (ctime(), addr_info[0]))

                # client로 응답을 돌려줌
                for socket_in_list in connection_list:
                    if socket_in_list != serverSocket and socket_in_list != sock:
                        try:
                            socket_in_list.send('[%s] 새로운 방문자가 대화방에 들어왔습니다. 반가워요~!' % ctime())
                        except Exception as e:
                            socket_in_list.close()
                            connection_list.remove(socket_in_list)
            # 접속한 사용자(client)로 부터 새로운 데이터 받음
            else:
                data = sock.recv(BUFSIZE)
                if data:
                    print('[INFO][%s] client로부터 데이터를 전달 받았습니다' % ctime())
                    for socket_in_list in connection_list:
                        if socket_in_list != serverSocket and socket_in_list != sock:
                            try:
                                socket_in_list.send('[%s] %s' % (ctime(), data))
                                print('[INFO][%s] client로 데이터를 전달합니다.' % ctime())
                            except Exception as e:
                                print(e.message)
                                socket_in_list.close()
                                connection_list.remove(socket_in_list)
                                continue
                else:
                    connection_list.remove(sock)
                    sock.close()
                    print('[INFO][%s] 사용자와의 연결이 끊어졌습니다.' % ctime())
    except KeyboardInterrupt:
        serverSocket.close()
        sys.exit()
