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
	print("Wrong number of parameters: “error: args should contain <ServerIP> <ServerPort> <Username>”")
else: 
	ClientSocket = socket.socket()
	host = sys.argv[1]
	## ================================= ip error ===============
	if valid_ip(host) == False:
		raise Exception("error: server ip invalid, connection refused.") from None
	## ================================ port error ===================
	try: 
		port = int(sys.argv[2])
	except ValueError:
		raise Exception("error: server port invalid, connection refused.") from None
	## ==================================================
	username = sys.argv[3]
	print('Waiting for connection')
	try:
		ClientSocket.connect((host, port))
	except socket.error as e:
		print("!!!!!!" + str(e))
	## ================================= check for username with wrong format ================

	## ================================= check for duplicated username ======================
	print(f'Sending username...')
	ClientSocket.send(str.encode(username))
	reply = ClientSocket.recv(2048)
	if reply == b'DUsername':
		# raise Exception("Error: Duplicated username!")
		username_valid = False
		print("username illegal, connection refused.")
		ClientSocket.send(str.encode('e'))
		reply_e = ClientSocket.recv(2048)
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


