import sys
import pickle
import socket

command = ['tweet', 'subscribe', 'unsubscribe', 'exit', 'timeline', 'getuser', 'gettweets']

def valid_ip(host):
    ip_arr = host.split('.')
    if len(ip_arr) != 4:
        return False

    for i in ip_arr:
        if i < 0 or i > 255:
            return False
    return True

def conenctionCheck(connection, argv):
    # username_valid = True
    # parameter_valid = True
    # error = False
    ##======================= number of parameter ==============
    if len(argv) != 4:
        sys.exit("Wrong number of parameters: “error: args should contain <ServerIP> <ServerPort> <Username>")
        return False
    ## ================================= ip error ===============
    ip = argv[1]
    if valid_ip(ip) == False:
        print("error: server ip invalid, connection refused.")
        return False
    ## ================================ port error ===================
    port = int(sys.argv[2])
    try:
        connection.connect((ip, port))
    except:
        print("error: server port invalid, connection refused.")
        return False
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



def tagChecker(hashtag):
    tagList = []
    for tag in hashtag:
        if len(tag) <= 0:
            return False
        tagList.append(tag)

    return tagList

def tweet(command, message, hashtag, user, connection):
    tagList = tagChecker(hashtag)

    if tagList:
        print("hashtag illegal format, connection refused")
        return 0

    if len(message) <= 0:
        print("message format illegal")
        return 0
    elif len(message) > 150:
        print("message length illegal, connection refused.")
        return 0

    tmp = (command, message, tagList, user)
    sendTweet = pickle.dump(tmp)
    connection.send(sendTweet)

def subscribe(command, hashtag, connection, user): # for both subscribe and unsubscribe
    tagList = tagChecker(hashtag)
    tmp = (command, tagList, user)
    subscribeSend = pickle.dump(tmp)
    connection.send(subscribeSend)

def main(argv):
    user = argv[3]
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection = conenctionCheck(clientSocket, argv) # check connection error
    if not connection:
        sys.exit(1)

    # check duplicate username from server
    clientSocket.send(user.encode())
    recvMsg = clientSocket.recv().decode() # reply from server whether username is duplicated
    if recvMsg:
        print("error: username has wrong format, connection refused.")
        clientSocket.close()
        sys.exit(1)

    inputList = []
    for line in sys.stdin:
        for x in line:
            inputList.append(x)
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

        if x[0] == 'tweet' and len(x) == 3:
            tweet(x[0], x[1], x[3], user, clientSocket)
            clientSocket.recv().decode()
        elif x[0] == 'subscribe' and len(x) == 2:
            subscribe(x[0], x[1], user, clientSocket)
            clientSocket.recv().decode()
        elif x[0] == 'unsubscribe'and len(x) == 2:
            subscribe(x[0], x[1], user, clientSocket)
            clientSocket.recv().decode()
        elif x[0] == 'timeline' and len(x) == 1:
            tmp = (x[0], clientSocket)
            timelineSend = pickle.dump(tmp)
            clientSocket.send(timelineSend)
            clientSocket.recv().decode()
        elif x[0] == 'getuser'and len(x) == 1:
            tmp = (x[0], clientSocket)
            getuserSend = pickle.dump(tmp)
            clientSocket.send(getuserSend)
            clientSocket.recv().decode()
        elif x[0] == 'gettweets' and len(x) == 1:
            tmp = (x[0], x[1], clientSocket)
            gettweetSend = pickle.dump(tmp)
            clientSocket.send(gettweetSend)
            clientSocket.recv().decode()
        elif x[0] == 'exit'and len(x) == 1:
            print("bye bye")
            break

    clientSocket.close()

if __name__ == "__main__":
    main(sys.argv[0:])