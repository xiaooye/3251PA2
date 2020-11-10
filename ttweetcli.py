import sys
import pickle
import socket


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
    print(argv)
    ##======================= number of parameter ==============
    if len(argv) != 4:
        sys.exit("Wrong number of parameters: “error: args should contain <ServerIP> <ServerPort> <Username>")
        sys.exit(1)
    ## ================================= ip error ===============
    if valid_ip(argv[1]) == False:
        print("error: server ip invalid, connection refused.")
        sys.exit(1)
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
        print("message format illegal, connection refused.")
        return 1
    elif len(message) > 150:
        print("message length illegal, connection refused.")
        return 1

    tmp = (op, tagList)
    sendTweet = pickle.dumps(tmp)
    connection.send(sendTweet)
    return 0


# =====================for both subscribe and unsubscribe========================
def subscribe(command, hashtag, op, connection):
    tagList = tagChecker(hashtag)
    if not tagList:
        print("hashtag illegal format, connection refused")
        return 1
    tmp = (op, tagList)
    subscribeSend = pickle.dumps(tmp)
    connection.send(subscribeSend)
    return 0


def main(argv):
    user = argv[3]
    op = {'user': None, 'msg': None, 'operation': None}
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ================ check connection error ====================
    connection = conenctionCheck(clientSocket, argv)
    if not connection:
        sys.exit(1)
    # ================check duplicate username from server==============
    z = (user, 'yea')
    y = pickle.dumps(z)
    clientSocket.send(y)
    # ==========reply from server whether username is duplicated, 0 for duplicated, 1 otherwise==========
    recvMsg = clientSocket.recv(1024).decode()
    print(recvMsg)
    if not int(recvMsg):
        print("error: username has wrong format, connection refused.")
        clientSocket.close()
        sys.exit(1)

    print("type whatever you want")
    # inputList = []
    for line in sys.stdin:
        print(line)
        # for x in line:
        #     inputList.append(x)
        # input = line.split('\"')
        # command = input[0].strip()
        #
        # if command == 'exist':
        #     print("bye bye")
        #     clientSocket.send(command.encode())
        #     break
        #
        # msg = input[1]
        #
        # hashtag = input[2].strip()
        x = line.split()
        command = x[0]
        op['operation'] = command
        op['user'] = user
        if command == 'tweet':
            # ==========tweet return 1 for error 0 otherwise==================
            y = tweet(line, op, clientSocket)
            if y:
                continue
            clientSocket.recv(1024).decode()
            print()
        elif command == 'subscribe' and len(x) == 2:
            y = subscribe(command, x[1], op, clientSocket)
            if y:
                continue
            clientSocket.recv(1024).decode()
            print()
        elif command == 'unsubscribe' and len(x) == 2:
            y = subscribe(command, x[1], op, clientSocket)
            if y:
                continue
            clientSocket.recv(1024).decode()
            print()
        elif command == 'timeline' and len(x) == 1:
            tmp = (op, None)
            timelineSend = pickle.dumps(tmp)
            clientSocket.send(timelineSend)
            clientSocket.recv(1024).decode()
            print()
        elif command == 'getuser' and len(x) == 1:
            # tmp = (command, user)
            # getuserSend = pickle.dumps(tmp)
            tmp = (op, None)
            getuserSend = pickle.dumps(tmp)
            clientSocket.send(getuserSend)
            clientSocket.recv(1024).decode()
            print()
        elif command == 'gettweets' and len(x) == 2:
            tmp = (op, None)
            gettweetSend = pickle.dumps(tmp)
            clientSocket.send(gettweetSend)
            clientSocket.recv(1024).decode()
            print()
        elif command == 'exit' and len(x) == 1:
            tmp = (op, None)
            exitSend = pickle.dumps(tmp)
            clientSocket.send(exitSend)
            print("bye bye")
            break

    clientSocket.close()


if __name__ == "__main__":
    main(sys.argv[0:])