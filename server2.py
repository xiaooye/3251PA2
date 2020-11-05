import socket
import os
from _thread import *
import threading
import sys

ServerSocket = socket.socket()
host = '127.0.0.1'
port = int(sys.argv[1]) 
ThreadCount = 0
usernames = set([])  # set
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    # ===================== lock ===========================
    data = ''
    my_lock = threading.Lock()
    username = connection.recv(2048)          # username
    print(f'username is : {username}')
    my_lock.acquire()
    if username in usernames:
        connection.send(str.encode("DUsername"))
        print(f'Deuplicated username@@')
    else: 
        usernames.add(username)
        connection.send(str.encode("username legal, connection established."))
    my_lock.release()
    print(f'usernames: {usernames}')

    connection.send(str.encode('Welcome to the Server\n'))

    while data != b'e':
        data = connection.recv(2048)        # may be 'e'
        reply = 'Server Says: ' + data.decode('utf-8')
        connection.send(str.encode(reply))
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()