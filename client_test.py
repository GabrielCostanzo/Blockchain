"""
# Echo client program
import socket
import pickle

HOST = 'localhost'    # The remote host
PORT = 8089           # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('Hello, world'.encode('UTF-8'))
data = s.recv(1024)
s.close()
print ('Received', pickle.loads(data))
"""

# Python TCP Client A
import socket 
import pickle
import time
import os

ip_list = []

def clear():
	os.system('cls' if os.name=='nt' else 'clear')

host = socket.gethostname() 
#host = '18.216.83.7'
client_ip = (socket.gethostbyname(socket.gethostname()))
print("client_ip:", client_ip)
port = 3389
BUFFER_SIZE = 1024
MESSAGE = ""

def ip_request():
	ip_num_selection = False
	eom_index = 0
	message_list = []
	while ip_num_selection == False:
		clear()
		ip_num = input("number of ips [1-100]: ")
		if int(ip_num) > 0 and int(ip_num) <= 100:
			MESSAGE = b"i"+str(ip_num).encode('UTF-8')+b"f"+client_ip.encode('UTF-8')
			ip_num_selection = True
	tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	tcpClientA.connect((host, port))
	data = b""
	try:
		tcpClientA.send(MESSAGE.encode('UTF-8'))     
	except:
		tcpClientA.send(MESSAGE)

	end = False
	blob = ""
	clear()
	print("received:\n")
	while end == False:
		data = tcpClientA.recv(BUFFER_SIZE)
		blob += data.decode('UTF-8')
		if data[-3:] == b"end":
			print("\nend of data stream")
			end = True
			break

	message_list = blob.split("\n\t\n\t")
	message_list.remove(message_list[-1])

	for i in message_list:
		if i not in ip_list:
			ip_list.append(i)
	#MESSAGE = input("tcpClientA: Enter message to continue/ Enter exit:").encode('UTF-8')
	print(ip_list)
	tcpClientA.close()

import pprint 
import json

def block_request():
	block_selection = False
	while block_selection == False:
		clear()
		block_num = input("Enter the highest block on record\n[0] for full blockchain: ")
		MESSAGE = b"b"+str(block_num).encode('UTF-8')+b"f"+client_ip.encode('UTF-8')
		if int(block_num) >= 0:
			block_selection = True
	tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	tcpClientA.connect((host, port))
	data = b""
	try:
		tcpClientA.send(MESSAGE.encode('UTF-8'))     
	except:
		tcpClientA.send(MESSAGE)

	end = False
	blob = b""
	clear()
	print("received:\n")
	while end == False:
		data = tcpClientA.recv(BUFFER_SIZE)
		blob += data

		if data[-3:] == b"end":
			print("\nend of data stream")
			end = True
			break

	message_blob = blob.split(b"\n\t\n\t")
	message_blob.remove(message_blob[-1])
	#pprint.pprint(json.loads(message_blob))
	for i in message_blob:
		pprint.pprint(json.loads(i))
	#MESSAGE = input("tcpClientA: Enter message to continue/ Enter exit:").encode('UTF-8')
	tcpClientA.close()

selection = False
while selection == False:
	clear()
	print("\n\n")
	print("request a list of ip connections: [0]")
	print("request an updated blockchain: [1]")
	print("request an updated mempool [2]")
	prefix = input("please enter a command: ")
	if prefix == "0":
		selection = True
	if prefix == "1":
		selection = True


if prefix == "0":
	ip_request()
if prefix == "1":
	block_request()
	 
