import socketserver
import threading

HOST = ''
PORT = 9010
lock = threading.Lock()

class UserManger:
    def __init__(self):
        self.users = {}
    def addUser(self, username, conn, addr):
        # if username in self.users:
        #     conn.send('이미 등록된 사용자 입니다.\n'.encode())
        #     return None
        
        lock.acquire()
        self.users[username] = (conn, addr) # key=username / values=conn, addr
        lock.release()

        # for key, value in self.users.items():
        #     print(key, ":", value)
        self.sendMessageToAll(username, '\n[%s]님이 입장했습니다.' % username)
        print('+++ 대화 참여자 수[%d]' % len(self.users))
        return username

    def messageHandler(self, username, msg):
        if msg[0] != '/':
            self.sendMessageToAll(username, '\n[%s] %s' % (username, msg))
            return

    def sendMessageToAll(self, username, msg):
        for conn, addr in self.users.values():
            # print(self.users[username][0])
            # print(conn)
            print('111111111111111')
            if self.users[username][0] != conn: # 중복 메시지 방지
                print('if if if if if')
                conn.send(msg.encode())
            print('222222222222222')

class MyTcpHandler(socketserver.BaseRequestHandler):
    usermanager = UserManger()

    def handle(self):
        print('[%s] 연결됨' % self.client_address[0])

        try:
            username = self.registerUsername()
            # msg = self.request.recv(1024)
            # print('zzz')
            while True:
                # self.request.send(('[%s] ' % username).encode())
                msg = self.request.recv(1024) # b'test' / type = byte
                # print('xxx')
                self.usermanager.messageHandler(username, msg.decode())
                print('[%s] %s' % (username, msg.decode())) # type = str

        except Exception as e:
            print(e)

    def registerUsername(self):
        while True:
            self.request.send('로그인 ID : '.encode())
            print('로그인 ID 기다리는 중...')
            username = self.request.recv(1024) # b'username'
            username = username.decode().strip() # strip() 얄옆 공백, \n 제거
            print('받음')
            # print('-----\n', username, '\n------\n')
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
