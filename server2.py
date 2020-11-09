import socketserver
import threading
import sys
import os

BUFFER_SIZE = 1024
MAX_CONN = 6
hashtag = {}
users = {}
message = {}

def spellingcheck():
    # check number of argument
    if (len(sys.argv) != 2 ):
        sys.exit("Wrong command")

    #check if port is vaild
    try:
        port = int(sys.argv[1])
    except ValueError:
        sys.exit("Invaild value for server port")

    # check port range
    if (port > 65535 or port <= 0):
        sys.exit("Value for server port exceeds limit")

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        if threading.active_count() > MAX_CONN:
            self.request.sendall('OFF Limit!'.encode('utf-8'))
        else:
            print('server get connection!')
            while True:
                data = self.request.recv(BUFFER_SIZE)
                if len(data)>0:
                    print('server read: TweetMessage{',data.decode('utf-8'),"}")
                    cur_thread = threading.current_thread()
                    print(threading.active_count())
                    self.request.sendall('response'.encode('utf-8'))
                    print('send:','response')                   

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def main():
    #check argument
    spellingcheck()

    #create socket
    port = int(sys.argv[1])
    server_address = ('localhost', port)

    server = ThreadedTCPServer(server_address, ThreadedTCPRequestHandler)

    #waiting for connection   
    try:
        print('server listening at ' + str(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print("server closed by admin")
        os._exit(1)
    


if __name__ == '__main__':
    main()
    