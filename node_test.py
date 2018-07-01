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

import ipgetter

client = pymongo.MongoClient()
db = client.database

#collection named posts:
blocks = db.blocks
ip_addresses = db.ip_addresses

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
                ipv4 = (ip_addresses.find_one({"_id": i})["ipv4"]).encode('UTF-8')
                print(ipv4, count)
                self.conn.sendall(ipv4 + b"\n\t\n\t")
            except TypeError:
                print("index error")
                self.conn.send(b"end\n\tend")
                return
        self.conn.send(b"end\n\tend")
        
        print("server delivered stored ips.\n")

    def blocks_deliver(self, start_height):
        print("blocks were requested from the server.")
        block_count = blocks.count()
        for i in range(start_height, block_count):
            current_block = blocks.find_one({"_id": i})
            if current_block == None:
                self.conn.sendall(b"end\n\tend")
                return
            sender_block = json.dumps(current_block).encode('UTF-8')

            print("size:", sys.getsizeof(sender_block))
            self.conn.sendall(sender_block + b"\n\t\n\t")

        self.conn.sendall(b"end\n\tend")
 
    def run(self): 
        closed = False
        f_index = 0
        num = 0
        client_ip = b""
        while True : 
            try:
                data = self.conn.recv(3389) 
            except ConnectionResetError:
                print("A connection was forcibly closed.")
                self.conn.close()
                closed = True
                server_thread.threads.remove(self)
                return 0

            if not data: 
                #os._exit(0)
                self.conn.close()
                server_thread.threads.remove(self)
                return 0

            if closed == False:
                try:
                    if str(chr(data[0])) == "i" or str(chr(data[0])) == "b":
                        for i in range(len(data)):
                            if str(chr(data[i])) == "f":
                                f_index = i
                        num = int(data[1:f_index])
                        client_ip = data[f_index+1:].decode('UTF-8')

                        search_ip = ip_addresses.find_one({"ipv4": client_ip})
                        if search_ip == None:
                            ip_addresses.insert_one({"_id": ip_addresses.count(), "ipv4": client_ip})

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
                    server_thread.threads.remove(self)
                    return 0
        conn.close()


# Python TCP Client A


class OutThread(Thread): 
 
    def __init__(self, host): 
        Thread.__init__(self) 

        self.host = host
        #self.host = socket.gethostname() 
        #self.host = '18.220.180.123'
        #self.client_ip = (socket.gethostbyname(socket.gethostname()))
        self.client_ip = ipgetter.myip()
        self.port = 3389
        self.BUFFER_SIZE = 1024
        self.MESSAGE = ""

    def clear(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def ip_request(self):
        ip_list = []
        ip_num_selection = False
        eom_index = 0
        message_list = []
        while ip_num_selection == False:
            self.clear()
            ip_num = input("number of ips [1-100]: ")
            if int(ip_num) > 0 and int(ip_num) <= 100:
                self.MESSAGE = b"i"+str(ip_num).encode('UTF-8')+b"f"+self.client_ip.encode('UTF-8')
                ip_num_selection = True
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        tcpClientA.settimeout(7)
        try:
            tcpClientA.connect((self.host, self.port))
        except socket.timeout:
            return 0
        data = b""
        try:
            tcpClientA.send(self.MESSAGE.encode('UTF-8'))     
        except:
            tcpClientA.send(self.MESSAGE)

        end = False
        blob = ""
        self.clear()
        print("received:\n")
        while end == False:
            data = tcpClientA.recv(self.BUFFER_SIZE)
            blob += data.decode('UTF-8')
            if data[-8:] == b"end\n\tend":
                end = True
                break

        message_list = blob.split("\n\t\n\t")
        message_list.remove(message_list[-1])

        for i in message_list:
            if i not in ip_list:
                ip_list.append(i)
        #MESSAGE = input("tcpClientA: Enter message to continue/ Enter exit:").encode('UTF-8')
        print(ip_list)

        for i in ip_list:
            search_ip = ip_addresses.find_one({"ipv4": i})
            if search_ip == None and str(search_ip) != str(self.client_ip):
                ip_addresses.insert_one({"_id": ip_addresses.count(), "ipv4": i})


        tcpClientA.close()


    def block_request(self):
        block_selection = False
        while block_selection == False:
            self.clear()
            block_num = input("Enter the highest block on record\n[0] for full blockchain: ")
            self.MESSAGE = b"b"+str(block_num).encode('UTF-8')+b"f"+self.client_ip.encode('UTF-8')
            if int(block_num) >= 0:
                block_selection = True
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        tcpClientA.settimeout(7)
        try:
            tcpClientA.connect((self.host, self.port))
        except socket.timeout:
            return 0
        data = b""
        try:
            tcpClientA.sendall(self.MESSAGE.encode('UTF-8'))     
        except:
            tcpClientA.send(self.MESSAGE)

        end = False
        blob = b""
        self.clear()
        print("received:\n")
        while end == False:
            data = tcpClientA.recv(self.BUFFER_SIZE)
            blob += data

            if data[-8:] == b"end\n\tend":
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

    def run(self):
        while True:
            selection = False
            while selection == False:
                self.clear()
                print("\n\n")
                print("request a list of ip connections: [0]")
                print("request an updated blockchain: [1]")
                print("request an updated mempool [2]")
                print("close thread [-1]")
                prefix = input("please enter a command: ")
                if prefix == "0":
                    selection = True
                elif prefix == "1":
                    selection = True
                elif prefix == "-1":
                    selection = True


            if prefix == "0":
                task = self.ip_request()
                if task == 0:
                    return 0 
            if prefix == "1":
                task = self.block_request()
                if task == 0:
                    return 0
            if prefix == "-1":
                return 0

            time.sleep(10)

connect = False
class Master_Server(Thread): 
    def __init__(self): 
        Thread.__init__(self) 
        # Multithreaded Python server : TCP Server Socket Program Stub
        self.TCP_IP = '0.0.0.0' 
        self.TCP_PORT = 3389
        self.BUFFER_SIZE = 1024  # Usually 1024, but we need quick response 

        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.tcpServer.bind((self.TCP_IP, self.TCP_PORT)) 
        self.threads = [] 

    def run(self):
        while True:
            while connect == False: 
                self.tcpServer.listen(4) 
                print ("Multithreaded Python server : Waiting for connections from TCP clients...")
                (conn, (ip,port)) = self.tcpServer.accept() 
                newthread = ClientThread(conn, ip, port) 
                newthread.start() 
                self.threads.append(newthread) 
                print(self.threads)
             
            for t in self.threads: 
                t.join() 


master_threads = []
local_host = socket.gethostname()

server_thread = Master_Server()
server_thread.start()
master_threads.append(server_thread)

out_client = OutThread(local_host)
out_client.start()
master_threads.append(out_client)

for t in master_threads:
    t.join()