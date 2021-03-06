import socket
import pickle
import queue
import threading

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ip='127.0.0.1'
port = 8080
add = (ip,port)

z = ('ajdiwjidj', 'yea')
y = pickle.dumps(z)

clientSocket.sendto(y,add)

input_queue = queue.Queue()

class ThreadingExample(object):
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
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            data = clientSocket.recv(1024)
            print(data)
            #data_queue.put(data)

class ThreadingExample1(object):
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
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            x = input()
            input_queue.put(x)

example = ThreadingExample()
example1 = ThreadingExample1()

count = 0

while True:
    try:
        x = input_queue.get_nowait()
        if x:
            print(x)
            clientSocket.sendto(y,add)
        #data = data_queue.get_nowait()
        #print(data)
    except queue.Empty:
        pass