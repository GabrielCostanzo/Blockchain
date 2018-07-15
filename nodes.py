import thread_manager
import socket
import ipgetter
import os
import time
import pymongo
from wallet_log import loaded_wallet, user_login
from thread_manager import block_load_switch
from json_serialize import block_to_json
import chain
from user import wallet
import json
import random

client = pymongo.MongoClient()
db = client.database

blocks = db.blocks
ip_addresses = db.ip_addresses
act_ips = db.act_ips
mem_pool = db.mem_pool

#local: "73.32.165.76"
#aws: "18.222.145.60"

print((socket.gethostbyname(socket.gethostname())), ipgetter.myip())

class node():
	def __init__(self, loaded_wallet):
		self.super_ips = ["18.222.145.60"]
		self.active_ips = []
		self.local_host = (socket.gethostbyname(socket.gethostname()))
		self.network_ip = ipgetter.myip()
		self.thread_master = []
		self.loaded_wallet = loaded_wallet

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
							out_client = thread_manager.request_thread(i, 0)
							out_client.start()
							if out_client.connection_status == True and i not in self.active_ips:
								self.active_ips.append(i)
						except:
							print("\nerror connecting to %s"%i)

				self.test_connections()
			if len(self.active_ips) > 0 and len(self.active_ips) < 8:
				for i in self.active_ips:
					if i != self.network_ip and i != self.local_host:
						try:
							out_client = thread_manager.request_thread(i, 0)
							out_client.start()
							if out_client.connection_status == True and i not in self.active_ips:
								self.active_ips.append(i)
						except:
							print("\nerror connecting to %s"%i)

				self.test_connections()	
				print("\nconnected to network!")
				print("\n\n%s"%self.active_ips)
				#os._exit(0)
				active_found = True


		print("\nnumber of active ips:", len(self.active_ips))
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
					out_client = thread_manager.request_thread(current_host, -1)
					out_client.start()
					if out_client.connection_status == True and out_client.host not in self.active_ips:
						self.active_ips.append(out_client.host)
					self.thread_master.append(out_client)
				except:
					print("\nerror connecting to %s"%current_host)

	def send_transaction(self):
		to_send = json.dumps(self.loaded_wallet.create_transaction(allen.serialized_public, 113, 12)).encode('UTF-8')
		for i in self.active_ips:
			sender_thread = thread_manager.SendThread(i, "transaction", to_send)
			sender_thread.start()


class super_node(node):
	def __init__(self, loaded_wallet):
		super().__init__(loaded_wallet)
		self.server_thread = thread_manager.server_thread()
		self.start_nonce = random.randint(0, 999999999999)
		def start_server(self):
			self.server_thread.start()
			self.thread_master.append(self.server_thread)
			self.network_connect()
			for i in range(2):
				self.request_blocks()
			mine_thread = thread_manager.mining_thread(self)
			mine_thread.start()

		start_server(self)


	def request_blocks(self):
		print("\nrequesting blocks")
		for i in self.active_ips:
			try:
				out_client = thread_manager.request_thread(i, 1)
				out_client.start()
			except:
				print("\nerror requesting blocks")

			while thread_manager.block_load_switch == False:
				time.sleep(1)
			return 



tim = wallet()
allen = wallet()
snode = super_node(loaded_wallet(user_login()))
