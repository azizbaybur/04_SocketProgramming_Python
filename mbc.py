from socket import *

MBS_ADDRESS = '127.0.0.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

message = raw_input('Type your request command:')

clientSocket.sendto(message,(MBS_ADDRESS, serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print modifiedMessage

msgsent1 = message.partition(":")[0]
msgsent2 = message.partition(":")[1]

msgreceived1 = modifiedMessage.partition(":")[0]
#msgreceived2 = modifiedMessage.partition(":")[1]

if(msgsent1=="REG" and msgreceived1 =="ACCEPT"):
    print "Successful user registration: " + msgsent2
elif (msgsent1=="REG" and msgreceived1 =="REJECT"):
    print "Rejected user registeration: " + msgsent2

clientSocket.close()
