import socketserver
import threading, queue
import sys
import os
import pickle

BUFFER_SIZE = 4096
MAX_CONN = 6
hashtags = {'ALL':set()}
threads = {}
users = {}
subcount = {}
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

def exit(user):
    users.pop(user)
    for x in hashtags:
        hashtags[x].remove(user)
    subcount.pop(user)

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        if threading.active_count() > MAX_CONN:
            self.request.sendall('Off Limit!'.encode('utf-8'))
        else:
            #new thread for incoming socket
            cur_thread = threading.current_thread()
            print('server get connection!')
            user = ''
            # while True:
            #     #receive data
            try:
                data = self.request[0]
                socket = self.request[1]
                    # print("some",user)
                    # global listeners
                    # if user in listeners:
                    #     print("okay")
                    #     while len(listeners[user]) != 0:
                    #         print("sending...")
                    #         mes = listeners[user].pop(0)
                    #         print(mes)
                    #         self.request.sendall(mes.encode('utf-8'))
            except ConnectionResetError:
                exit(user)

                #if has data
                # if self.request:
                #unpack data
            data = pickle.loads(data)
            
            #if only one variable then create new user
            if (data[1] == 'yea'):
                user = data[0]      
                print(
                    "server read: TweetMessage{username='" + user + "', message='null', hashTags='null', operation='init'}")

                #check if user exists
                if user in users:
                    socket.sendto('d'.encode('utf-8'),self.client_address)
                else:
                    users[user] = set()
                    subcount[user] = 0
                    threads[user] = self.client_address
                    socket.sendto('username legal, connection established'.encode('utf-8'), self.client_address)
                
            else:
                d = data[0]
                message = d['msg']
                operation = d['operation']
                user = d['user']
                hashtag = data[1]

                #tweet
                if operation == 'tweet':
                    
                    #add tweet to collections                           
                    index = len(tweets)
                    tweets[index] = message

                    #add to sent history
                    users[user].add(index)
                    
                    #server message
                    print("server read: TweetMessage{username='" + user + "', message='" + message + "', hashTags='" + str(hashtag) + "', operation='tweet'}")

                    #construct receiver list
                    receiver = {}
                        
                    #iterate through hashtag list
                    for hash in hashtag:
                        if hash in hashtags:
                            for user in hashtags[hash]:
                                if user not in receiver:
                                    receiver[user] = hash

                    #send to each user
                    for user in receiver:
                        msg = pickle.dumps((message, receiver[user]))
                        socket.sendto(msg,threads[user])
                    
                    socket.sendto('success'.encode('utf-8'),self.client_address)

                elif operation == 'subscribe':
                    #server message
                    print("server read: TweetMessage{username='" + user + "', message='null', hashTags='" + str(hashtag) + "', operation='subscribe'}")

                    #iterate through hashtags
                    for hash in hashtag:
                        #check if reach limit
                        if subcount[user] >= 3:
                            socket.sendto('subscribe out of limit'.encode('utf-8'),self.client_address)
                            break
                        else:
                            subcount[user] += 1
                            #create new hashtag
                            if hash not in hashtags:
                                hashtags[hash] = set([user])
                            else:
                                hashtags[hash].add(user)
                        socket.sendto('success'.encode('utf-8'),self.client_address)                          

                else:
                    print("some")
                    socket.sendto('error'.encode('utf-8'),self.client_address)

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
