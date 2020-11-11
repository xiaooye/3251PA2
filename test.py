import socketserver
import sys
import os

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

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        print(data)
        message = "data yeah"
        print(message)
        socket.sendto(message.encode(), self.client_address)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

def main():
    # check argument
    spellingcheck()

    # create socket
    port = int(sys.argv[1])
    server_address = ('localhost', port)

    server = ThreadedUDPServer(server_address, ThreadedUDPRequestHandler)

    # waiting for connection
    try:
        print('server listening at ' + str(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print("server closed by admin")
        os._exit(1)


if __name__ == '__main__':
    main()