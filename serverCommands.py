from http import client
import sys
import socket
import select

HOST = "***.***.***.***" 
PORT = 9999

#Get the type of socket ready
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #IP4 and SOCK_STREAM is TCP
#Bind to the socket
serverSocket.bind((HOST,PORT)) #the strange paranteces is becaus IP4 is a tuple
serverSocket.listen(5) #Listen to the socket for connection


while True:
    theSocket, address = serverSocket.accept()
    print(f"Connection from {address}")
    theSocket.send(bytes("Hello there","utf-8"))
    theSocket.close()


print("Done")
