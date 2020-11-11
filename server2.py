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
                    resp = pickle.dumps(('duplicate',None))
                    socket.sendto(resp,self.client_address)
                else:
                    users[user] = set()
                    subcount[user] = 0
                    threads[user] = self.client_address
                    timeline[user] = []
                    resp = pickle.dumps(("init", 'username legal, connection established'))
                    socket.sendto(resp, self.client_address)
                
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
                        has += ha
                    send_msg = (user + ':"' + message + '" ' + has)
                    tweets[index] = send_msg

                    #add to sent history
                    users[user].add(index)
                    
                    #server message
                    print(read(user,message,str(hashtag),"tweet"))

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
                        timeline[user].append(index)
                        user_msg = (user + ': "' + message + '" #' + receiver[user])
                        msg = pickle.dumps(("receive", user_msg))
                        socket.sendto(msg,threads[user])
                    
                    print(write("true", "tweet", "null", message , has , user , "null", 0, 0))

                #operation
                elif operation == 'subscribe':
                    #server message
                    print(read(user,"null",str(hashtag),"subscribe"))

                    #iterate through hashtags
                    for hash in hashtag:
                        #check if reach limit
                        if subcount[user] >= 3:
                            resp = pickle.dumps(("error", 'subscribe out of limit'))
                            socket.sendto(resp,self.client_address)
                            break
                        else:
                            subcount[user] += 1
                            #create new hashtag
                            if hash not in hashtags:
                                hashtags[hash] = set([user])
                            else:
                                hashtags[hash].add(user)
                        resp = pickle.dumps(("subscribe", "operation success"))
                        socket.sendto(resp,self.client_address)
                        print(write("true", "subscribe", "null", "null", "null", "null", "null", 0, 0))

                elif operation == "unsubscribe":
                    #server message
                    print(read(user,"null",str(hashtag),"unsubscribe"))
                    finish = True
                    #iterate through hashtags
                    for hash in hashtag:
                        try:
                            hashtags[hash].remove(user)
                        except KeyError:
                            pass

                    if finish:
                        print(write("true", "unsubscribe", "null", "null", "null", "null", "null", 0, 0))
                        socket.sendto('success'.encode(),self.client_address)
                
                elif operation == "timeline":
                    #server message
                    print(read(user,"null","null","timeline"))
                    timelines = []
                    for tweet in timeline[user]:
                        timelines.append(tweets[tweets])
                    tl = pickle.dumps(timeline)
                    socket.sendto(tl,self.client_address)

                elif operation == "getuser":
                    #server message
                    print(read(user,"null","null","getusers"))
                    us = []
                    for user in users:
                        us.append(user)
                    us = pickle.dumps(us)
                    socket.sendto(us,self.client_address)

                elif operation == "gettweets":
                    #server message
                    print(read(user,"null","null","gettweets"))
                    gett = []
                    for tweet in users[user]:
                        gett.append(tweets[tweet])
                    gett = pickle.dumps(gett)
                    socket.sendto(gett,self.client_address)
                    print(write("true", "gettweets", "null", "null", "null", "null", "null", 0, len(gett)))

                elif operation == "exit":
                    #server message
                    print(read(user,"null","null","exit"))
                    exit(user)
                    resp = pickle.dumps(("exit", "bye bye"))
                    socket.sendto(resp,self.client_address)                    

                else:
                    print("wrong command")
                    socket.sendto('error'.encode(),self.client_address)

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
