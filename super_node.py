import node_network
import socket
import ipgetter
import os
import time
import pymongo
from wallet_log import loaded_wallet
from wallet_log import user_login
from node_network import block_load_switch
"""
master_threads = []
local_host = socket.gethostname()

server_thread = node_network.Master_Server()
server_thread.start()
master_threads.append(server_thread)

out_client = node_network.OutThread(local_host)
out_client.start()
master_threads.append(out_client)

for t in master_threads:
    t.join()
"""

client = pymongo.MongoClient()
db = client.database

#collection named posts:
blocks = db.blocks
ip_addresses = db.ip_addresses

#local: "73.32.165.76"
#aws: "18.222.145.60"

print((socket.gethostbyname(socket.gethostname())), ipgetter.myip())

class node():
	def __init__(self):
		self.super_ips = ["testtest", "18.222.145.60", "testtesttest"]
		self.active_ips = []
		self.local_host = (socket.gethostbyname(socket.gethostname()))
		self.network_ip = ipgetter.myip()
		self.thread_master = []

	def network_connect(self):
		active_found = False
		self.test_connections()
		while active_found == False:
			if len(self.active_ips) < 8:
				for i in self.super_ips:
					if i != self.network_ip and i != self.local_host:
						try:
							out_client = node_network.OutThread(i, 0)
							out_client.start()
							if out_client.connection_status == True and i not in self.active_ips:
								self.active_ips.append(i)
						except:
							print("error connecting to %s"%i)

				self.test_connections()
			if len(self.active_ips) > 0 and len(self.active_ips) < 8:
				for i in self.active_ips:
					if i != self.network_ip and i != self.local_host:
						try:
							out_client = node_network.OutThread(i, 0)
							out_client.start()
							if out_client.connection_status == True and i not in self.active_ips:
								self.active_ips.append(i)
						except:
							print("error connecting to %s"%i)

				self.test_connections()	
				print("connected to network!")
				print("\n\n%s"%self.active_ips)
				#os._exit(0)
				active_found = True
		return 

	def test_connections(self):
		for i in range(ip_addresses.count()):
			current_host = ip_addresses.find_one({"_id": i})["ipv4"]
			if current_host != self.network_ip and current_host != self.local_host:
				try:
					out_client = node_network.OutThread(current_host, -1)
					out_client.start()
					if out_client.connection_status == True and out_client.host not in self.active_ips:
						self.active_ips.append(out_client.host)
					self.thread_master.append(out_client)
				except:
					print("error connecting to %s"%current_host)


class super_node(node):
	def __init__(self, loaded_wallet):
		node.__init__(self)
		self.server_thread = node_network.Master_Server()
		self.loaded_wallet = loaded_wallet

		def start_server(self):
			self.server_thread.start()
			self.thread_master.append(self.server_thread)
			self.network_connect()
			self.get_block_count()
			#time.sleep(60)
			#os._exit(0)
		start_server(self)


	def get_block_count(self):
		print("get blocks")
		for i in self.active_ips:
			try:
				out_client = node_network.OutThread(i, 1)
				out_client.start()
			except:
				print("error requesting blocks")

			while node_network.block_load_switch == False:
				time.sleep(1)
			return 




snode = super_node(loaded_wallet(user_login()))
#snode.start_server()
#snode.network_connect()

#print(snode.local_host)

#snode.test_connections()