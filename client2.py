import socket
import sys


def valid_ip(host):
		ip_arr = host.split('.')
		if len(ip_arr) != 4:
			return False
		for i in range(4):
			x = 0
			try: x = int(ip_arr[i])
			except: return False
			if x < 0 or x > 255:
				return False
		return True


username_valid = True
parameter_valid = True
##======================= number of parameter ==============
if len(sys.argv) != 4:
	sys.exit("Wrong number of parameters: “error: args should contain <ServerIP> <ServerPort> <Username>”")
ClientSocket = socket.socket()
host = sys.argv[1]
## ================================= ip error ===============
# if valid_ip(host) == False:
# 	print("error: server ip invalid, connection refused.")
# 	sys.exit(1)
## ================================ port error ===================
try: 
	port = int(sys.argv[2])
except ValueError:
	sys.exit("error: server port invalid, connection refused.")
# port range
if port < 0 or port > 60000:  # ?????????????????
	sys.exit("error: server port invalid, connection refused.")
## ======================== check for username format ==========================
username = sys.argv[3]
if username.isalnum() == False:
	sys.exit("error: username has wrong format, connection refused.")
print('Waiting for connection')
## ===================== ip error: connection error =====================
try:
	ClientSocket.connect((host, port))
except socket.error as e:
	sys.exit("error: server ip invalid, connection refused.")
## ================================= check for duplicated username ======================
print(f'Sending username...')
ClientSocket.send(str.encode(username))
reply = ClientSocket.recv(2048)     # Dusername OR username legal, connection established
if reply == b'DUsername':
	# username_valid = False
	# print("username illegal, connection refused.")
	# ClientSocket.send(str.encode('e'))
	# reply_e = ClientSocket.recv(2048)
	sys.exit("User is already logged in: “username illegal, connection refused.")
else: # username success: login successful
	print(reply)
## ===============================================================

if username_valid == True:
	Response = ClientSocket.recv(1024)   # welcome to ...
	print(Response)
	while True:
		Input = input('Say Something: ')
		ClientSocket.send(str.encode(Input))
		Response = ClientSocket.recv(1024)
		print(Response.decode('utf-8'))

ClientSocket.close()


