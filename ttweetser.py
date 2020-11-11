import socketserver
import threading, queue
import sys
import os
import pickle

BUFFER_SIZE = 4096
MAX_CONN = 6
hashtags = {'ALL':set()}
threads = {}
timeline = {}
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
    #we will collect all tweets anonymously with no user tag (but we also store the sender in the body of each tweet XD)
    users.pop(user)
    for x in hashtags:
        if user in hashtags[x]:
            hashtags[x].remove(user)
    threads.pop(user)
    timeline.pop(user)
    subcount.pop(user)

def read(user,message,hashtag,operation):
    return "server read: TweetMessage{username='" + user + "', message='" + message + "', hashTags='" + hashtag + "', operation='" + operation + "'}"

def write(success,type,error,tweetMsg,hashTags,sender,notification,usernames,historyMessages):
    return "server write: TweetResponse{success='" + success + "', type='"+ type +"', error='" + error +"', tweetMsg='"+tweetMsg+"', hashTags='" + hashTags + "', sender='"+sender+"', notification='"+notification+"', usernames="+ str(usernames) +", historyMessages="+ str(historyMessages) +"}"

def sender(self,type,data,socket):
    resp = pickle.dumps((type,data))
    socket.sendto(resp,self.client_address)

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        socket = self.request[1]

        if len(threads) > MAX_CONN:
            socket.sendto('Off Limit!'.encode(),self.client_address)
        else:
            user = ''

            #unpack data
            data = pickle.loads(data)
            
            #if only one variable then create new user
            if (data[1] == 'yea'):
                print("server get connection!")
                user = data[0]      
                print(read(user,"null","null","init"))

                #check if user exists
                if user in users:
                    sender(self,"duplicate","",socket)
                elif user == "":
                    sender(self,"uerror","error: username has wrong format, connection refused.",socket)
                else:
                    users[user] = set()
                    subcount[user] = 0
                    threads[user] = self.client_address
                    timeline[user] = []
                    sender(self,"init","username legal, connection established",socket)
                
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
                    has = ""
                    for ha in hashtag:
                        has += ("#" + ha)
                    send_msg = (user + ': "' + message + '" ' + has)
                    tweets[index] = send_msg

                    #add to sent history
                    users[user].add(index)
                    
                    #server message
                    print(read(user,message,str(hashtag),"tweet"))

                    #construct receiver list
                    receiver = set()
                        
                    #iterate through hashtag list
                    for hash in hashtag:
                        if hash in hashtags:
                            for auser in hashtags[hash]:
                                receiver.add(auser)

                    #send to each user
                    for getuser in receiver:
                        timeline[getuser].append(index)
                        msg = pickle.dumps(("receive", send_msg))
                        socket.sendto(msg,threads[getuser])
                    
                    sender(self,"tweet","",socket)
                    print(write("true", "tweet", "null", message , has , user , "null", 0, 0))

                #operation
                elif operation == 'subscribe':
                    #server message
                    print(read(user,"null",str(hashtag),"subscribe"))

                    #iterate through hashtags
                    for hash in hashtag:
                        #check if reach limit
                        if subcount[user] >= 3:
                            mess = 'operation failed: sub #' + hash + ' failed, already exists or exceeds 3 limitation'
                            sender(self,"error",mess,socket)
                            print(write("false", "subscribe", mess , "null", "null", "null", "null", 0, 0))
                            break
                        else:
                            subcount[user] += 1
                            #create new hashtag
                            if hash not in hashtags:
                                hashtags[hash] = set([user])
                            else:
                                if user not in hashtags[hash]:
                                    hashtags[hash].add(user)
                                else:
                                    mess = 'operation failed: sub #' + hash + ' failed, already exists or exceeds 3 limitation'
                                    sender(self,"error",mess,socket)
                                    print(write("false", "subscribe", "null", "null", "null", "null", "null", 0, 0))
                                    break
                        sender(self,"subscribe","operation success",socket)
                        print(write("true", "subscribe", "null", "null", "null", "null", "null", 0, 0))

                elif operation == "unsubscribe":
                    #server message
                    print(read(user,"null",str(hashtag),"unsubscribe"))
                    #iterate through hashtags
                    for hash in hashtag:
                        try:
                            hashtags[hash].remove(user)
                        except KeyError:
                            pass

                    sender(self,"unsubscribe","operation success",socket)
                    print(write("true", "unsubscribe", "null", "null", "null", "null", "null", 0, 0))                      
                
                elif operation == "timeline":
                    #server message
                    print(read(user,"null","null","timeline"))
                    for tweet in timeline[user]:
                        sender(self,"timeline",tweets[tweet],socket)

                elif operation == "getusers":
                    #server message
                    print(read(user,"null","null","getusers"))
                    for user in users:
                        sender(self,"getusers",user,socket)            

                elif operation == "gettweets":
                    #server message
                    print(read(user,"null","null","gettweets"))
                    for tweet in users[user]:
                        sender(self,"gettweets",tweets[tweet],socket)  
                    print(write("true", "gettweets", "null", "null", "null", "null", "null", 0, len(users[user])))

                elif operation == "exit":
                    #server message
                    print(read(user,"null","null","exit"))
                    exit(user)
                    # sender(self,"exit","bye bye",socket)

                else:
                    print("wrong command")
                    sender(self,"error","wrong command",socket)

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
