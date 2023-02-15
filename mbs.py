from socket import *

MBS_PORT = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('', MBS_PORT))


user = list()
password = list()
board = list()
content = list()

def registeration(username, passs):
	modifiedMessage = ""

	if username in user :
		modifiedMessage = "REJECT:" + username
	else:
		user.append(username)
		password.append(passs)
		modifiedMessage = "ACCEPT:" + username
	return modifiedMessage


def create(boardname):
	modifiedMessage = ""

	if boardname in board:
		modifiedMessage = "REJECT:" + boardname
	else:
		modifiedMessage = "ACCEPT:" + boardname
		board.append(boardname)
	return modifiedMessage

	

def printBoards():
	modifiedMessage = "LIST:BOARDS:"

	for i in board:
		modifiedMessage += i

	return modifiedMessage

########################################################################################################################################	
def printMessagesByBoardname(boardname):
	modifiedMessage = "MESSAGE:"
	if boardname in content:
			modifiedMessage = modifiedMessage + ":" + content[i][2] + ":" + content[i][1] + ":" + content[i][0] + ":" + content[i][3]
########################################################################################################################################

def idValidity(username, passs):
	valid = 0
	if username in user:
		valid = 1

	return valid

def boardValidity(boardname):
	valid = 0
	if boardname in board:
		valid = 1

	return valid



print ("MBS Started")
#######
i = 0
#######
while 1:
		message, clientAddress = serverSocket.recvfrom(2048)
		request = message.decode("utf-8").partition(":")[0]

		if  request == "REG":
			_ , username,passs = message.decode("utf-8").split(":")
			print ("Registration request arrived from user " + username)
			modifiedMessage = registeration(username, passs)

			if modifiedMessage.partition(":")[0] == "ACCEPT":
				print ("Successful user registeration: " + str(username))
			else:
				print ("Rejectted user registeration: " + username)

		elif request == "CREATE":
			_,boardname = message.decode("utf-8").split(":")
			modifiedMessage = create(boardname)
			if (modifiedMessage.partition(":")[0] == "ACCEPT"):
				print (boardname + " message board was created.")
			else:
				print (boardname + " message board couldnt be created.")

		elif request == "LIST":
			modifiedMessage = printBoards()

		elif request == "ADD":
			_, username, passs, boardname, msgContent = message.decode("utf-8").split(":")

			validId = idValidity(username,passs)
			validBoard = boardValidity(boardname)

			if validId == 1 and validBoard == 1:
				modifiedMessage = "ACCEPT:" + username + ":" + boardname + ":" + msgContent

				print (username + "added the message '" + msgContent + "' on " + boardname + " message board.")
				content.append(msgContent)
				####################################################
				content.append([i, username, boardname, msgContent]) #yukarıdaki komut yerine çoklu item append etmem lazım
				####################################################
			elif validId == 0 and validBoard == 1:
				modifiedMessage = "REJECT::" + boardname + ":" + msgContent

			elif validId == 1 and validBoard == 0:
				modifiedMessage = "REJECT:" + username + "::" + msgContent

			elif validId == 0 and validBoard == 0:
				modifiedMessage = "REJECT:::" + msgContent
		
		################################################################################		
		elif(request=="MESSAGE"):
			boardname = message.partition(":")[1]
			modifiedMessage = printMessagesByBoardname(boardname)
		################################################################################		
		
		else:
			modifiedMessage = "Command is not valid. Try again."

		serverSocket.sendto(modifiedMessage.encode(), clientAddress)