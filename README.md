# 3251PA2

#PLEASE SET THE TIMEOUT (time.sleep(1)) OF STD_IN FUNCTION TO AT LEAST ONE SECOND TO PREVENT DELAY!!!!

# High level implementation
The Twitter server is implemented with multi-threading to allow connections between the server and multiple clients concurently. Twitter clients allows various functionalities including tweeting a post along with hashtags, subscribing and unsubscribing to hashtags, printing out all informations on tweets, users, and senders. Most importantly, the subscribers should be able to receive tweets simultaniously while the clients tweet under the respective hashtags. Each client program contains three threads. Thread 1 is responsible for checking the format of client input as well as performing tweeting, subscribing, unsubscribing, and outputting tweets and user information functionalities. The second thread runs concurently to receive the tweets with corresponding hashtags and print the tweets on the console. Thread 3 runs in the background in order to receive any user inputs from the console. 
The server program contains dictionaries with hashtags as keys and a list of subscribers of the hashtags as the key. When a new tweets with multiple hashtags is posted, users in the list of these specific tweets are put into a set to prevent users receiving duplicated tweets. A new dictionary is created everytime a new hashtag is created. Each dictionary is populated as clients subscribing to the hashtags of the corresponding dictionary. In order to keep track of timeline, out team implemented two dictionaries. The first dictionary contains users as keys and numbers as values. The second dictionary has numbers as keys and the content of the tweet as well as hashtags as values. The user, which is the key for the frist dictionary, have the same values as the keys in dictionary 2 if this user tweeted the content in the second dictionary. 

# Teammates
We Xin: 
We Xin is responsible for server side programming, including creating, implementing and populating the dictionaries and lists in server program and receiving or sending information to the client program.  

Zhuobin Yang:
Zhuobin Yang is charge for client side programming, including implementing the "subscribe", "unsubscribe", "timeline", and "gettweets" functions.

Peiqi Zhao:
Peiqi Zhao is responsible for error checking of user inputs, "tweet" and "exit" functions, and documentations. 

# How to use 
#PLEASE SET THE TIMEOUT (time.sleep(1)) OF STD_IN FUNCTION TO AT LEAST ONE SECOND TO PREVENT DELAY!!!!

For the server program, enter "ttweetser <Port Number>" into the console will start the server program. ("<>" should not be inputted into the console).
In order to connect to the server, the client side need to enter "ttweetcli <ServerIP> <ServerPort> <Username>" into the console.
On the client side console, client is able to tweet a post with "tweet “<content of post(less than 150 characters)>” <Hashtag>", where "" is necessary around the message.
Entering "subscribe <Hashtag>" and "unsubscribe <Hashtag>" in to the client console allows client to subscribe or unsubscribe to a specific hashtag. 
Entering "timeline" into the client console prints the user who tweeted the posts, content of the tweet and hashtags to the client side.
Entering "getusers" into the client console prints all users who are currently logged in.
Entering "gettweets <Username>" into the client console prints out all tweets which are posted by the username. 
To terminate the connection with the server for a client, enter "exit" to the client concole.
 
# Dependent packages 
All imports in the Twitter are common used imports including os, pickle, socket, treading, and queue. Some users might need to install "pickle" on their system with command "pip install pickle-mixin".
