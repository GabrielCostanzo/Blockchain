# Echo server program
import socket 
from threading import Thread 
from socketserver import ThreadingMixIn 
import random 
import pickle
import os
import datetime
from multiprocessing import Queue
import time

import pymongo
import json

import pprint
import sys
client = pymongo.MongoClient()
db = client.database

#collection named posts:
blocks = db.blocks

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0' 
TCP_PORT = 3389
BUFFER_SIZE = 1024  # Usually 1024, but we need quick response 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
connect = False

connected_ips = []
message_list = [b"23.23.2.45", b"424.2.3.78", b"983.1.4.93", b"23.24.2.455", b"42.235.3.78", b"98.135.4.93",
b"23.2.3.45", b"42.4.3.78", b"98.1.4.03", b"25.2.2.45", b"52.2.3.78", b"98.0.4.93",
b"23.2.4.45", b"42.5.3.78", b"98.1.4.13", b"26.2.2.45", b"42.2.3.78", b"98.12.4.93",
b"23.2.5.45", b"42.6.3.78", b"98.1.4.23", b"27.2.2.45", b"32.2.3.78", b"98.114.4.93",
b"23.2.6.45", b"42.7.3.78", b"98.1.4.33", b"28.2.2.45", b"22.2.3.78", b"98.145.4.93",
b"23.2.7.45", b"42.2.3.78", b"98.1.4.43", b"29.2.2.45", b"12.2.3.78", b"98.178.4.93"]

class ClientThread(Thread): 
 
    def __init__(self,conn,ip,port): 
        Thread.__init__(self) 
        self.conn = conn
        self.ip = ip 
        self.port = port 
        print ("[+] New server socket thread started for " + ip + ":" + str(port))
        connect = True

    def ips_deliver(self, count):
        print("ips were requested from server.")
        for i in range(count):
            try:
                print(message_list[i], count)
                self.conn.sendall(message_list[i] + b"\n\t\n\t")
            except IndexError:
                print("index error")
                self.conn.send(b"end")
                return
        self.conn.send(b"end")
        
        print("server delivered stored ips.\n")

    def blocks_deliver(self, start_height):
        print("blocks were requested from the server.")
        block_count = blocks.count()
        for i in range(start_height, block_count):
            current_block = blocks.find_one({"_id": i})
            if current_block == None:
                self.conn.sendall(b"end")
                return
            sender_block = json.dumps(current_block).encode('UTF-8')

            print("size:", sys.getsizeof(sender_block))
            self.conn.send(sender_block + b"\n\t\n\t")

        self.conn.send(b"end")
 
    def run(self): 
        closed = False
        f_index = 0
        num = 0
        client_ip = b""
        while True : 
            try:
                data = conn.recv(3389) 
            except ConnectionResetError:
                print("A connection was forcibly closed.")
                self.conn.close()
                closed = True
                threads.remove(self)
                return 0

            if not data: 
                #os._exit(0)
                self.conn.close()
                threads.remove(self)
                return 0

            if closed == False:
                try:
                    if str(chr(data[0])) == "i" or str(chr(data[0])) == "b":
                        for i in range(len(data)):
                            if str(chr(data[i])) == "f":
                                f_index = i
                        num = int(data[1:f_index])
                        client_ip = data[f_index+1:]

                        if client_ip not in message_list:
                            connected_ips.append([client_ip, self])
                            message_list.append(client_ip)

                        if str(chr(data[0])) == "i":
                            self.ips_deliver(num)
                        elif str(chr(data[0])) == "b":
                            self.blocks_deliver(num)


                    else:
                        #print ("Server received data:", data)
                        MESSAGE = b"not a valid command"
                        self.conn.send(MESSAGE)  # echo 
                except ConnectionResetError:
                    print("A connection was forcibly closed.")
                    self.conn.close()
                    threads.remove(self)
                    return 0
        conn.close()

while connect == False: 
    tcpServer.listen(4) 
    print ("Multithreaded Python server : Waiting for connections from TCP clients...")
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(conn, ip, port) 
    newthread.start() 
    threads.append(newthread) 
    print(threads)
 
for t in threads: 
    t.join() 

"""
while 1:
    #recieve data from client
    data = conn.recv(1024)
    if not data: break
    print ('Received:', data, "from client.")
    #send data to client 
    conn.send(pickle.dumps(deal(2)))

conn.close()
"""

