import socketserver
import threading
import sys
import os
import pickle

BUFFER_SIZE = 4096
MAX_CONN = 6
hashtags = {'ALL':set()}
users = {}
tweets = {}


def spellingcheck():
    # check number of argument
    if (len(sys.argv) != 2):
        sys.exit("Wrong command")

    # check if port is vaild
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
            self.request.sendall('Off Limit!'.encode('utf-8'))
        else:
            #new thread for incoming socket
            cur_thread = threading.current_thread()
            print('server get connection!')
            while True:
                #receive data
                data = self.request.recv(BUFFER_SIZE)
                #if has data
                if len(data) > 0:
                    #unpack data
                    data = pickle.loads(data)
                    #if only one variable then create new user
                    if (len(data) == 2):
                        print('server get connection!')
                        user = data[0].strip()
                        print(
                            "server read: TweetMessage{username='" + user + "', message='null', hashTags='null', operation='init'}")

                        #check if user exists
                        if user in users:
                            self.request.sendall('duplicate'.encode('utf-8'))
                        else:
                            users[user] = set()
                            self.request.sendall('true'.encode('utf-8'))

                        #tmp
                        print(users)

                    elif (len(data) == 3):
                        print(data)
                        self.request.sendall('response'.encode('utf-8'))
                    else:
                        print(data)
                else:
                    break


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main():
    # check argument
    spellingcheck()

    # create socket
    port = int(sys.argv[1])
    server_address = ('localhost', port)

    server = ThreadedTCPServer(server_address, ThreadedTCPRequestHandler)

    # waiting for connection
    try:
        print('server listening at ' + str(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print("server closed by admin")
        os._exit(1)


if __name__ == '__main__':
    main()
