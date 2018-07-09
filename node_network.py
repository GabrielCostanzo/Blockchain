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

import block_verification
from user import encrypt_key
from user import sign 
from user import master_key

client = pymongo.MongoClient()
db = client.database

#collection named posts:
blocks = db.blocks
ip_addresses = db.ip_addresses
mem_pool = db.mem_pool
act_ips = db.act_ips

block_load_switch = False

class ClientThread(Thread): 
 
    def __init__(self,conn,ip,port): 
        Thread.__init__(self) 
        self.conn = conn
        self.ip = ip 
        self.port = port 
        #print ("[+] New server socket thread started for " + ip + ":" + str(port))
        connect = True

    def ips_deliver(self, count):
        #print("ips were requested from server.")
        for i in range(count):
            try:
                ipv4 = (ip_addresses.find_one({"_id": i})["ipv4"]).encode('UTF-8')
                #print(ipv4, count)
                self.conn.sendall(ipv4 + b"\n\t\n\t")
            except TypeError:
                #print("index error")
                self.conn.send(b"end\n\tend")
                return
        self.conn.send(b"end\n\tend")
        
        print("server delivered stored ips.\n")

    def blocks_deliver(self, start_height):
        #print("blocks were requested from the server.")
        block_count = blocks.count()
        for i in range(start_height, block_count):
            current_block = blocks.find_one({"_id": i})
            if current_block == None:
                self.conn.sendall(b"end\n\tend")
                return
            sender_block = json.dumps(current_block).encode('UTF-8')

            #print("size:", sys.getsizeof(sender_block))
            self.conn.sendall(sender_block + b"\n\t\n\t")

        self.conn.sendall(b"end\n\tend")

    def distribute_transaction(self, out_data):
        out_points = act_ips.find({})
        print("out_points:", act_ips.count())
        for i in out_points:
            relay_thread = SendThread(i["_id"], "transaction", out_data)
            relay_thread.start()
            print("transaction relay initiated for %s"% i["_id"])


    def receive_transaction(self, transaction):
        try:
            mem_pool.insert_one({"_id": encrypt_key(transaction, master_key), "t_data": transaction})
            print("received transaction added to mem_pool")
            print(mem_pool.count())
            time.sleep(2)
            self.conn.sendall(b"your transaction has been considered by a node.")
            self.conn.sendall(b"end\n\tend")
            self.distribute_transaction(transaction) 
        except:
            print("error adding received transaction to mempool: (possible duplicate)")
            self.conn.sendall(b"your transaction has been considered by a node.")
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
                return 0

            if not data: 
                #os._exit(0)
                self.conn.close()
                return 0

            if closed == False:
                try:
                    if str(chr(data[0])) == "i" or str(chr(data[0])) == "b" or str(chr(data[0])) == "t":
                        for i in range(len(data)):
                            if str(chr(data[i])) == "f":
                                f_index = i
                        payload = data[1:f_index]
                        try:
                            client_ip = data[f_index+1:].decode('UTF-8')

                            search_ip = ip_addresses.find_one({"ipv4": client_ip})
                            dot_count = search_ip.count(".")
                            local_find = search_ip[:7]
                            if search_ip == None and dot_count == 3 and local_find != "10.0.0.":
                                ip_addresses.insert_one({"_id": ip_addresses.count(), "ipv4": client_ip})
                        except:
                            pass
                        if str(chr(data[0])) == "i":
                            self.ips_deliver(int(payload))
                        elif str(chr(data[0])) == "b":
                            self.blocks_deliver(int(payload))
                        if str(chr(data[0])) == "t":
                            self.receive_transaction(payload)


                    else:
                        #print ("Server received data:", data)
                        MESSAGE = b"not a valid command"
                        self.conn.send(MESSAGE)  # echo 
                except ConnectionResetError:
                    print("A connection was forcibly closed.")
                    self.conn.close()
                    return 0
        self.conn.close()


# Python TCP Client A


class OutThread(Thread): 
 
    def __init__(self, host, command): 
        Thread.__init__(self) 

        self.host = host
        self.connection_status = False
        #self.host = socket.gethostname() 
        #self.host = '18.220.180.123'
        #self.client_ip = (socket.gethostbyname(socket.gethostname()))
        self.client_ip = ipgetter.myip()
        self.port = 3389
        self.BUFFER_SIZE = 1024
        self.MESSAGE = ""
        self.command = command
        self.tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.timeout_secs = 7
        self.tcpClientA.settimeout(self.timeout_secs)
        try:
            self.tcpClientA.connect((self.host, self.port))
            print("Sucessfully connected to %s"%self.host)
            self.connection_status = True
        except:
            print("failed to connect to %s."%self.host)
            self.command = -1

    def clear(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def ip_request(self):
        ip_list = []
        ip_num_selection = False
        eom_index = 0
        message_list = []
        while ip_num_selection == False:
            #self.clear()
            # number of ips to be received
            ip_num = 10
            if int(ip_num) > 0 and int(ip_num) <= 100:
                self.MESSAGE = b"i"+str(ip_num).encode('UTF-8')+b"f"+self.client_ip.encode('UTF-8')
                ip_num_selection = True

        data = b""
        try:
            self.tcpClientA.send(self.MESSAGE.encode('UTF-8'))     
        except:
            self.tcpClientA.send(self.MESSAGE)

        end = False
        blob = ""
        #self.clear()
        print("received:\n")
        while end == False:
            data = self.tcpClientA.recv(self.BUFFER_SIZE)
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


        self.tcpClientA.close()

    def block_request(self):
        global block_load_switch
        block_load_switch = False
        print("blocks requested")
        block_selection = False
        while block_selection == False:
            #self.clear()
            block_num = int(blocks.count())
            #block_num = input("Enter the highest block on record\n[0] for full blockchain: ")
            self.MESSAGE = b"b"+str(block_num).encode('UTF-8')+b"f"+self.client_ip.encode('UTF-8')
            if int(block_num) >= 0:
                block_selection = True

        data = b""
        try:
            self.tcpClientA.sendall(self.MESSAGE.encode('UTF-8'))     
        except:
            self.tcpClientA.send(self.MESSAGE)

        end = False
        blob = b""
        #self.clear()
        print("received:\n")
        while end == False:
            data = self.tcpClientA.recv(self.BUFFER_SIZE)
            blob += data

            if data[-8:] == b"end\n\tend":
                print("\nend of data stream")
                end = True
                break

        message_blob = blob.split(b"\n\t\n\t")
        message_blob.remove(message_blob[-1])
        #pprint.pprint(json.loads(message_blob))
        for i in range(0, len(message_blob)-1):
            search_block = blocks.find_one({"_id":json.loads(message_blob[i])["height"]})

            if search_block == None:
                front_block = json.loads(message_blob[i].decode('UTF-8'))
                follow_block = json.loads(message_blob[i+1].decode('UTF-8'))
                validity_check = block_verification.verify_block(front_block, follow_block)
                if validity_check == True:
                    blocks.insert_one(front_block)
                    print("added block: %s"%front_block["height"])
                    if i == len(message_blob[-1]):
                        blocks.insert_one(follow_block)
                        print("added final block: %s"%follow_block["height"])
            else:
                follow_block = json.loads(message_blob[i+1].decode('UTF-8'))
                validity_check = block_verification.verify_block(search_block, follow_block)
                blocks.insert_one(follow_block)
                print("appended: %s"% follow_block["height"])

        block_load_switch = True
        #MESSAGE = input("tcpClientA: Enter message to continue/ Enter exit:").encode('UTF-8')
        self.tcpClientA.close()

    def run(self):
        while True:

            if self.command == 0:
                self.ip_request()
                return 0 
            if self.command == 1:
                self.block_request()
                return 0
            if self.command == -1:
                return 0

class SendThread(Thread): 
 
    def __init__(self, host, command, send_load): 
        Thread.__init__(self) 

        self.host = host
        self.connection_status = False
        #self.host = socket.gethostname() 
        #self.host = '18.220.180.123'
        #self.client_ip = (socket.gethostbyname(socket.gethostname()))
        self.client_ip = ipgetter.myip()
        self.port = 3389
        self.BUFFER_SIZE = 1024
        self.MESSAGE = ""
        self.command = command
        self.tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.timeout_secs = 7
        self.tcpClientA.settimeout(self.timeout_secs)
        self.send_load = send_load
        try:
            self.tcpClientA.connect((self.host, self.port))
            print("Send Thread connected to %s"%self.host)
            self.connection_status = True
        except:
            print("Send Thread failed to connect to %s."%self.host)
            self.command = -1

    def send_transaction(self):
        data = b""
        end = False
        self.MESSAGE = b"t"+self.send_load+b"f"+self.client_ip.encode('UTF-8')        
        try:
            self.tcpClientA.sendall(self.MESSAGE.encode('UTF-8'))     
        except:
            self.tcpClientA.send(self.MESSAGE)

        #self.clear()
        print("received:\n")
        while end == False:
            data += self.tcpClientA.recv(self.BUFFER_SIZE)
            if data[-8:] == b"end\n\tend":
                #print("\nend of data stream")
                print(data[:-8])
                end = True
                break

        self.tcpClientA.close()

    def run(self):
        if self.command == "transaction":
            self.send_transaction()
            return 0 


class Master_Server(Thread): 
    def __init__(self): 
        Thread.__init__(self) 
        # Multithreaded Python server : TCP Server Socket Program Stub
        self.TCP_IP = '0.0.0.0' 
        self.TCP_PORT = 3389
        self.BUFFER_SIZE = 1024  # Usually 1024, but we need quick response 
        self.connect = False

        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.tcpServer.bind((self.TCP_IP, self.TCP_PORT)) 
        self.threads = [] 

    def run(self):
        while True:
            while self.connect == False: 
                self.tcpServer.listen(4) 
                #print ("Multithreaded Python server : Waiting for connections from TCP clients...")
                (conn, (ip,port)) = self.tcpServer.accept() 
                newthread = ClientThread(conn, ip, port) 
                newthread.start() 
                self.threads.append(newthread) 
                #print(self.threads)
             
            for t in self.threads: 
                t.join() 


"""
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
"""