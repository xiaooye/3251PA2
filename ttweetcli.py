import sys
import os
import pickle
import socket
import threading
import queue

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
input_queue = queue.Queue()
address = None
user = ""

class userInput(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = None                           # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            try:
                x = input()
                # if x == "exit":
                #     op = {'user': user, 'msg': None, 'operation': "exit"}
                #     exitSend = pickle.dumps((op, None))
                #     clientSocket.sendto(exitSend, address)
                #     print("bye bye")
                #     os._exit(1)
                input_queue.put(x)
            except KeyboardInterrupt:
                op = {'user': user, 'msg': None, 'operation': "exit"}
                exitSend = pickle.dumps((op, None))
                try:
                    clientSocket.sendto(exitSend, address)
                except ConnectionResetError:
                    os._exit(1)
                os._exit(1)

class receive(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = None                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            try:
                data = clientSocket.recv(4096)
            except ConnectionResetError:
                print("error: server port invalid, connection refused.")
                os._exit(1)
            t, d = pickle.loads(data)
            if t == "duplicate":
                print("username illegal, connection refused.")
                os._exit(1)
            elif t == "uerror":
                print(d)
                os._exit(1)
            elif t == "init":
                print(d)
            elif t == "receive":
                print(d)
            elif t == "subscribe":
                print(d)
            elif t == "unsubscribe":
                print(d)
            elif t == "gettweets":
                print(d)
            elif t == "getusers":
                print(d)
            elif t == "timeline":
                print(d)
            elif t == "exit":
                print("bye bye")
                os._exit(1)
            elif t == "error":
                print(d)
            else:
                pass

# ==============ip address check for validation===========================
def valid_ip(host):
    ip_arr = host.split('.')
    if len(ip_arr) != 4:
        return False

    for i in ip_arr:
        i = int(i)
        if i < 0 or i > 255:
            return False
    return True

def conenctionCheck(connection, argv):
    # username_valid = True
    # parameter_valid = True
    # error = False
    ##======================= number of parameter ==============
    if len(argv) != 4:
        print("error: args should contain <ServerIP> <ServerPort> <Username>")
        os._exit(1)
    ## ================================= ip error ===============
    if valid_ip(argv[1]) == False:
        print("error: server ip invalid, connection refused.")
        os._exit(1)
    ## ================================ port error ===================
    ip = argv[1]
    port = int(argv[2])
    try:
        connection.connect((ip, port))
    except:
        print("error: server port invalid, connection refused.")
        sys.exit(1)
    return True
    ## ======================== check for username format ==========================
    # username = sys.argv[3]
    # if username.isalnum() == False:
    #     sys.exit("error: username has wrong format, connection refused.")
    # print('Waiting for connection')
    ## ===================== ip error: connection error =====================
    # try:  ## ????????????????????????????????????????????
    #     connection.connect((host, port))
    # except socket.error as e:
    #     sys.exit("error: server ip invalid, connection refused.")


# ===============check for valid hashtag======================
def tagChecker(hashtag):
    tagList = []
    for tag in hashtag:
        if len(tag) <= 0:
            return False
        tagList.append(tag)

    return tagList


def tweet(line, op, connection):

    list = line.split("\"")
    message = list[1]
    op['msg'] = message
    hashtag = filter(None,list[2].strip().split("#"))
    tagList = tagChecker(hashtag)

    if not tagList:
        print("hashtag illegal format, connection refused")
        return 1

    if len(message) <= 0:
        print("message format illegal")
        return 1
    elif len(message) > 150:
        print("message length illegal, connection refused.")
        return 1

    tmp = (op, tagList)
    sendTweet = pickle.dumps(tmp)
    connection.sendto(sendTweet,address)
    return 0


# =====================for both subscribe and unsubscribe========================
def subscribe(command, hashtag, op, connection):
    hashtag = filter(None,hashtag.strip().split("#"))
    tagList = tagChecker(hashtag)
    if not tagList:
        print("hashtag illegal format, connection refused")
        return 1
    tmp = (op, tagList)
    subscribeSend = pickle.dumps(tmp)
    connection.sendto(subscribeSend,address)
    return 0


def main(argv):
    global address
    global user
    connection = conenctionCheck(clientSocket, argv)
    user = argv[3]
    op = {'user': None, 'msg': None, 'operation': None}
    # ================ check connection error ====================
    ip = argv[1]
    port = int(argv[2])
    address = (ip,port)
    if not connection:
        os._exit(1)
    # ================check duplicate username from server==============
    else:
        z = (user, 'yea')
        y = pickle.dumps(z)
        clientSocket.sendto(y,address)
    # ==========reply from server whether username is duplicated, 0 for duplicated, 1 otherwise==========
    # if recvMsg == "d":
    #     print("error: username has wrong format, connection refused.")
    #     clientSocket.close()
    #     sys.exit(1)

    receiveMsg = receive()
    input = userInput()

    #print("type whatever you want")
    # inputList = []

    while True:
        try:
            line = input_queue.get_nowait()
            # if x:
            #     clientSocket.sendto(y, add)
            x = line.split()
            command = x[0]
            op['operation'] = command
            op['user'] = user
            if command == 'tweet':
                # ==========tweet return 1 for error 0 otherwise==================
                y = tweet(line, op, clientSocket)

            elif command == 'subscribe' and len(x) == 2:
                y = subscribe(command, x[1], op, clientSocket)

            elif command == 'unsubscribe' and len(x) == 2:
                y = subscribe(command, x[1], op, clientSocket)

            elif command == 'timeline' and len(x) == 1:
                tmp = (op, None)
                timelineSend = pickle.dumps(tmp)
                clientSocket.sendto(timelineSend, address)

            elif command == 'getusers' and len(x) == 1:
                # tmp = (command, user)
                # getuserSend = pickle.dumps(tmp)
                tmp = (op, None)
                getuserSend = pickle.dumps(tmp)
                clientSocket.sendto(getuserSend, address)

            elif command == 'gettweets' and len(x) == 2:
                tmp = (op, None)
                gettweetSend = pickle.dumps(tmp)
                clientSocket.sendto(gettweetSend, address)

            elif command == 'exit' and len(x) == 1:
                tmp = (op, None)
                exitSend = pickle.dumps(tmp)
                clientSocket.sendto(exitSend, address)
                print("\nbye bye")
                os._exit(1)
            # data = data_queue.get_nowait()
            # print(data)
            else:
                print("invaild argument\n")

        except queue.Empty:
            pass
            
        except KeyboardInterrupt:
            op = {'user': user, 'msg': None, 'operation': "exit"}
            exitSend = pickle.dumps((op, None))
            try:
                clientSocket.sendto(exitSend, address)
            except ConnectionResetError:
                os._exit(1)
            os._exit(1)
   
    clientSocket.close()


if __name__ == "__main__":
    main(sys.argv[0:])