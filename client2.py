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
error = False;
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
try: ## ????????????????????????????????????????????
	ClientSocket.connect((host, port))
except socket.error as e:
	sys.exit("error: server ip invalid, connection refused.")
## ================================= check for duplicated username ======================
print(f'Sending username...')
ClientSocket.send(str.encode(username))
reply = ClientSocket.recv(2048)     # Dusername OR username legal, connection established
if reply == b'DUsername':
	sys.exit("User is already logged in: “username illegal, connection refused.")
else: # username success: login successful
	print(f'reply: f{reply}')
## ===============================================================
while True:
	error = False
	Input = input('Say Something: ')    # input: tweet​ “<150 char max tweet>” <Hashtag>
	## ========================================== tweet ==================================================
	if Input[0: 5] == 'tweet':    # post a tweet; check length
		input_arr = Input.split('#')
		print(f'input_arr: {input_arr}')
		if len(input_arr) >= 6 or len(input_arr) == 1:     # if hashtages more than 5 #
			print("Illegal hashtag: “hashtag illegal format, connection refused.”-----more than 5 hashtages or no hashtage")
			error = True;
		else: 
			for i in range(1, len(input_arr)):      # each hash more than 1 but less than 15
				if len(input_arr[i]) == 0 or len(input_arr[i]) >= 14 or input_arr[i].isalnum() == False:
					print("Illegal hashtag: “hashtag illegal format, connection refused.”-----length less than 1 or more than 15/letter + number")
					error = True;
					break;
			
			# check for ""
			message_arr = input_arr[0].split('"')
			print(f'message_arr: {message_arr}')
			if len(message_arr) <= 1 or len(message_arr[1]) == 0:     # no "" exsit
				print("Illegal message length(=0 or None): “message format illegal.”----no "" or content")
				error = True;
	## ============================================= tweet end ================================================

	if error == False: 		
		ClientSocket.send(str.encode(Input))
		# Response = ClientSocket.recv(1024)
		# print(Response.decode('utf-8'))
	if Input == "exit":
		Response = ClientSocket.recv(1024)
		print(Response.decode('utf-8'))
		break

ClientSocket.close()


