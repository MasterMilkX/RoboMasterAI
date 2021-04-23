import socket
import random

'''
ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()
'''

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 6969

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

resp = ClientSocket.recv(1024)
while True:
    sent = "W - " + str(random.randint(0,4)) + "," + str(random.randint(0,4))
    ClientSocket.send(str.encode(sent))
    resp = ClientSocket.recv(1024)
    print(resp.decode('utf-8'))

ClientSocket.close()