import socket
import os
from _thread import *
import random
import time
import numpy as np

''' INITIAL
ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
	ServerSocket.bind((host, port))
except socket.error as e:
	print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
	connection.send(str.encode('Welcome to the Server'))
	while True:
		data = connection.recv(2048)
		reply = 'Server Says: ' + data.decode('utf-8') + " :)"
		if not data:
			break
		connection.sendall(str.encode(reply))
	connection.close()

while True:
	Client, address = ServerSocket.accept()
	print('Connected to: ' + address[0] + ':' + str(address[1]))
	start_new_thread(threaded_client, (Client, ))
	ThreadCount += 1
	print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
Client.close()
'''

# BASIC GRID MOVEMENT
grid_size = 4
blank_grid = []
for r in range(grid_size):
	a = []
	for c in range(grid_size):
		a.append('.')
	blank_grid.append(a)

grid = blank_grid.copy()

X = [2,0]

def showGrid():
	os.system('clear')

	for r in grid:
		print(r)

def updateGrid():
	grid = blank_grid.copy()
	grid[X[1]][X[0]] = 'X'

def changePos():
	X = [random.randint(0,grid_size),random.randint(0,grid_size)]
	updateGrid()
	print("new!")


def hop():
	changePos()
	showGrid()


starttime = time.time()
#threading.Timer(1.0, hop).start()


#setup server
ServerSocket = socket.socket()
host = '127.0.0.1'
port = 6969
ThreadCount = 0

try:
	ServerSocket.bind((host, port))
except socket.error as e:
	print(str(e))

ServerSocket.listen(5)


def threaded_client(connection):
	#connection.send(str.encode('Welcome to the Server'))
	while True:
		data = connection.recv(2048)
		if not data:
			break

		dataSp = data.split(" - ")
		ch = dataSp[0]
		posStr = dataSp[1].split(",")
		pos = [int(posStr[0]),int(posStr[1])]

		reply = "* valid * "
		if(grid[pos[1]][pos[0]] != '.'):
			reply = "! invalid !"

		connection.sendall(str.encode(reply))
	connection.close()

while True:
	hop()

	Client, address = ServerSocket.accept()
	print('Connection from: ' + address[0] + ':' + str(address[1]))
	start_new_thread(threaded_client, (Client, ))
	ThreadCount += 1
	print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
Client.close()

