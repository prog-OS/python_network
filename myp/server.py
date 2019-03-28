import socketserver
import threading

HOST = ''
PORT = 9009
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
        return username

class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManger()

    def handle(self):
        print('[%s] 연결됨' % self.client_address[0])

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
