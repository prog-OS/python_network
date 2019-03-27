import socketserver
from os.path import exists

HOST = ''
PORT = 9009

class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data_transferred = 0
        print('[%s]연결된' %self.client_address[0])
        filename = self.request.recv(1024) # client로 부터 파일 이름 전달 받음
        filename = filename.decode() # 파일이름 이진 바이트 스트림 데이터를 일반 문자열로

        if not exists(filename):
            return

        print('파일[%s] 전송 시작...' %filename)
        with open(filename, 'rb') as f:
            try:
                data = f.read(1024)
                while data:
                    data_transferred += self.request.send(data)
                    data = f.read(1024)
            except Exception as e:
                print(e)

        print('전송완료[%s], 전송량[%d]' %(filename, data_transferred))

def runServer():
    print('파일 서버 시작')
    print('종료시 ctrl + c')

    try:
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('파일 서버 종료')

runServer()