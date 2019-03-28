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
        self.users[username] = (conn, addr)
        lock.release()

        print('+++ 대화 참여자 수[%d]' % len(self.users))
        return username

class MyTcpHandler(socketserver.BaseRequestHandler):
    usermanager = UserManger()

    def handle(self):
        print('[%s] 연결됨' % self.client_address[0])

        try:
            username = self.registerUsername()
            # msg = self.request.recv(1024)
            # while msg:
            #     print(msg.decode())
            #     msg = self.request.recv(1024)

        except Exception as e:
            print(e)

    def registerUsername(self):
        while True:
            self.request.send('로그인 ID : '.encode())
            username = self.request.recv(1024) # b'username'
            username = username.decode().strip() # strip() 얄옆 공백, \n 제거
            print('-----\n', username, '\n------\n')
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
