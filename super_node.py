import node_network
import socket
import ipgetter
import os
import time
import pymongo
from wallet_log import loaded_wallet
from wallet_log import user_login
from node_network import block_load_switch
from json_serialize import block_to_json
import chain
from user import wallet
import pickle
import json
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
act_ips = db.act_ips
mem_pool = db.mem_pool

#local: "73.32.165.76"
#aws: "18.222.145.60"

print((socket.gethostbyname(socket.gethostname())), ipgetter.myip())

class node():
	def __init__(self):
		self.super_ips = ["18.222.145.60"]
		self.active_ips = []
		self.local_host = (socket.gethostbyname(socket.gethostname()))
		self.network_ip = ipgetter.myip()
		self.thread_master = []

	def network_connect(self):
		act_ips.remove({})
		mem_pool.remove({})
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


		print("IP LEN:", len(self.active_ips))
		for i in self.active_ips:
			act_ips.insert_one({"_id": i})
		return 

	def test_connections(self):
		for i in range(ip_addresses.count()):
			current_host = ip_addresses.find_one({"_id": i})["ipv4"]
			dot_count = current_host.count(".")
			local_find = current_host[:7]
			if current_host != self.network_ip and current_host != self.local_host and dot_count == 3 and local_find != "10.0.0.":
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
			self.get_block_count()
			mine_thread = node_network.MiningThread(self)
			mine_thread.start()
			#input("\npress enter to send transaction\n")
			#self.send_transaction()
			#input("\npress enter to send block\n")
			#self.send_block()
			#input("\npress enter to exit\n")
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

	def send_transaction(self):
		to_send = json.dumps(self.loaded_wallet.create_transaction(allen.serialized_public, 113, 12)).encode('UTF-8')
		for i in self.active_ips:
			sender_thread = node_network.SendThread(i, "transaction", to_send)
			sender_thread.start()

	def send_block(self):
		mempool = []
		block_count = blocks.count()
		last_block = blocks.find_one({"_id": block_count - 1})
		to_send = block_to_json(chain.block(last_block, mempool, self.loaded_wallet.serialized_public, 0)).encode('UTF-8')
		for i in self.active_ips:
			sender_thread = node_network.SendThread(i, "block", to_send)
			sender_thread.start()

tim = wallet()
allen = wallet()
snode = super_node(loaded_wallet(user_login()))
#snode.start_server()
#snode.network_connect()

#print(snode.local_host)

#snode.test_connections()