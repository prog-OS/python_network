import socketserver
import threading
import os

HOST = ''
PORT = 9010
lock = threading.Lock()

class UserManger:
    def __init__(self):
        self.users = {}
    def addUser(self, username, conn, addr):
        if username in self.users:
            conn.send('이미 등록된 사용자 입니다.\n'.encode())
            return None
        
        lock.acquire()
        self.users[username] = (conn, addr) # key=username / values=(conn, addr)
        lock.release()

        # for key, value in self.users.items():
        #     print(key, ":", value)
        self.sendMessageToAll(username, '\n[%s]님이 입장했습니다.' % username)
        print('+++ 대화 참여자 수[%d]' % len(self.users))
        
        return username

    def removeUser(self, username):
        print('removeUser : [%s]' % username)
        if username not in self.users:
            return

        self.sendMessageToAll(username, '\n[%s]님이 퇴장했습니다.' % username)
        
        lock.acquire()
        del self.users[username]
        lock.release()
        
        print('-- 대화 참여자 수 [%d]' % len(self.users))
    
    def messageHandler(self, username, msg):

        if msg.strip() == '/quit':
            # print('나갈때 찍혀야됨')
            self.removeUser(username)
            return -1
        
        self.sendMessageToAll(username, '\n[%s] %s' % (username, msg))

    def sendMessageToAll(self, username, msg):
        print('<<<------------- sendMessageToAll --------------')
        for conn, addr in self.users.values():
            if self.users[username][0] != conn: # 중복 메시지 방지
                conn.send(msg.encode())
        print('------------- sendMessageToAll -------------->>>')


class MyTcpHandler(socketserver.BaseRequestHandler):
    usermanager = UserManger()

    def handle(self):
        print('[%s] 연결됨' % self.client_address[0])

        try:
            username = self.registerUsername()
            print("permission")
            self.request.send("permission".encode())
            
            while True:
                msg = self.request.recv(1024) # b'test' / type = byte
<<<<<<< HEAD

=======
                # print('handle : [%s]' % msg.decode())
                # print('xxx')
>>>>>>> 0442d2f0adce5c05765fbf3fdd285d77cb262125
                if self.usermanager.messageHandler(username, msg.decode()) == -1:
                    self.request.close()
                    break

                print('[%s] %s' % (username, msg.decode())) # type = str

        except Exception as e:
            print(e)

        print('[%s] 접속종료' % self.client_address[0])
        self.usermanager.removeUser(username)

    def registerUsername(self):
        while True:
            self.request.send('로그인 ID : '.encode())
            username = self.request.recv(1024) # b'username'
            username = username.decode().strip() # strip() 양옆 공백, \n 제거
            
            if self.usermanager.addUser(username, self.request, self.client_address):
                return username


class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def runServer():
    print('+++ 채팅서버를 시작합니다.++')
    print('+++ 끝내려면 ctrl + c')

    try:
        server = ChatingServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('--- 채팅 서버 종료')
        server.shutsown()
        server.server_close()

runServer()
