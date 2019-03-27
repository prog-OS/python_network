import socketserver
import threading

HOST = ''
PORT = 9009
lock = threading.Lock()

class UserManager:
    # 사용자관리 및 채팅 메세지 전송을 담당하는 클래스
    # ① 채팅 서버로 입장한 사용자의 등록
    # ② 채팅을 종료하는 사용자의 퇴장 관리
    # ③ 사용자가 입장하고 퇴장하는 관리
    # ④ 사용자가 입력한 메세지를 채팅 서버에 접속한 모두에게 전송
    def __init__(self):
        self.users = {}
    def addUser(self, username, conn, addr):
        if username in self.users:
            conn.send('이미 등록된 사용자 입니다.\n'.encode())
            return None

        lock.acquire()
        self.users[username] = (conn, addr)
        lock.release()

        self.sendMessageToAll('[%s]님이 입장했습니다.'%username)
        print('+++ 대화 참여자 수[%d]' %len(self.users))

        return username

    def removeUser(self, username):
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        self.sendMessageToAll('[%s]님이 퇴장했습니다.' %username)
        print('--- 대화 참여자 수 [%d]' %len(self.users))

    def messageHandler(self, username, msg):
        if msg[0] != '/':
            self.sendMessageToAll('[%s] %s' %(username, msg))
            return

        if msg.strip() == '/quit':
            self.removeUser(username)
            return -1

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())

class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    def handle(self): # client와 연결될 때 호출
        print('[%s] 연결됨' %self.client_address[0])

        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
                print(msg.decode())
                if self.userman.messageHandler(username, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)

        except Exception as e:
            print(e)

        print('[%s] 접속종료' %self.client_address[0])
        self.userman.removeUser(username)

    def registerUsername(self):
        while True:
            self.request.send('로그인ID : '.encode())
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.userman.addUser(username, self.request, self.client_address):
                return username

class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def runServer():
    print('+++ 채팅 서버를 시작합니다.')
    print('+++ 끝내려면 ctrl + c')

    try:
        server = ChatingServer((HOST, PORT), MyTcpHandler)
        server.serve_forever() # client의 접속 요청을 수신 대기, 수락수 
    except KeyboardInterrupt:
        print('--- 채팅 서버를 종료')
        server.shutdown()
        server.server_close()

runServer()