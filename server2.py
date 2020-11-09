import socketserver
import weakref
import threading
import sys

BUFFER_SIZE = 1024
MAX_CONN = 5
accepted_sockets = weakref.WeakSet()
hashtag = {}
users = {}
message = {}

def count_connections(self):
     return sum(1 for sock in accepted_sockets if sock.fileno() >= 0)

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
        if count_connections(self) >= MAX_CONN:
            self.request.sendall('OFF Limit!'.encode('utf-8'))
        else:
            address,pid = self.client_address
            accepted_sockets.add(self.client_address)
            print('server get connection!')
            while True:
                data = self.request.recv(BUFFER_SIZE)
                if len(data)>0:
                    print('receive=',data.decode('utf-8'))
                    cur_thread = threading.current_thread()
                    self.request.sendall('response'.encode('utf-8'))
                    print('send:','response')
                else:
                    print('Empty Message')
                    break

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def main():
    #check argument
    spellingcheck()

    #create socket
    port = int(sys.argv[1])
    server_address = ('localhost', port)

    server = ThreadedTCPServer(server_address, ThreadedTCPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    #waiting for connection
    print('server listening at ' + str(port))
    server.serve_forever()
    
            

# def threaded_client(connection):
#     # ===================== lock ===========================
#     tweet_message = ""
#     data = ''
#     my_lock = threading.Lock()
#     username = connection.recv(2048)          # username
#     print(f'username is : {username}')
#     my_lock.acquire()
#     if user in users:
#         connection.send(str.encode("DUsername"))
#         print(f'Deuplicated username@@')
#     else: 
#         users.add(username)
#         connection.send(str.encode("username legal, connection established."))
#     my_lock.release()
#     print(f'usernames: {users}')


#     while data != b'e':
#         data = connection.recv(2048)        # may be 'e'
#         reply = 'Server Says: ' + data.decode('utf-8')
#         connection.send(str.encode(reply))
#     connection.close()

if __name__ == '__main__':
    main()
