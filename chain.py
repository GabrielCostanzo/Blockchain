import datetime
from user import transaction, wallet, encrypt_key, sign, master_key
import pickle
from json_serialize import transaction_to_json
import json

class coinbase_transaction(transaction):
	def __init__(self, sender_public_key, receiver_public_key, input_amount, fees, block_height):
		super().__init__(sender_public_key, receiver_public_key, input_amount, fees)
		self.block_height = block_height
		self.status = "coinbase"
		self.transaction_data = pickle.dumps(self).decode('latin1')
		self.txid = encrypt_key(pickle.dumps(self), master_key).encode('UTF-8')
		#print(self.txid)

		def reward_calculator(self, block_height):
			base_reward = 50
			block_cut_rate = 210000
			block_cut_magnitude = 0.5
			if block_height < block_cut_rate:
				self.output_amount = base_reward
			else:
				self.output_amount = base_reward*(block_cut_magnitude**(int(self.block_height/block_cut_rate)))
		
		reward_calculator(self, self.block_height)




class genesis_block():
	def __init__(self, miner_public_key, start_nonce):
		self.block_hash = None
		self.height = 0

		self.coinbase_transaction = json.loads(transaction_to_json(coinbase_transaction(miner_public_key, miner_public_key, 0, 0, self.height)))
		self.transaction_fees = self.coinbase_transaction["fees"]
		self.block_reward = self.coinbase_transaction["output_amount"]
		self.total_output = self.block_reward


		self.previous_block_hash = b'0'*32
		self.merkle_root = (encrypt_key(json.dumps(self.coinbase_transaction).encode('UTF-8'), master_key)).encode('UTF-8')
		self.nonce = None

		self.timestamp = datetime.datetime.now() 

		self.transactions = [self.coinbase_transaction]

		self.miner_public_key = miner_public_key


		def proof_of_work(self, nonce, target):
			proof = False

			while proof == False:
				encoded_nonce = str(nonce).encode('UTF-8')
				prehash_base = (self.previous_block_hash+self.merkle_root+encoded_nonce)
				test_proof = encrypt_key(prehash_base, master_key)
				if test_proof[0:len(target)] == target:
					proof = True
				else:
					nonce += 1

			self.nonce = str(nonce).encode('UTF-8')
			self.block_hash = test_proof.encode('UTF-8')

		proof_of_work(self, start_nonce, '000')


class merkle_node():
	def __init__ (self, parent):
		self.child_left = None
		self.child_right = None
		self.parent = parent


class block():
	def __init__(self, json_previous_block, raw_transactions, miner_public_key, start_nonce):
		self.block_hash = None
		self.height = json_previous_block["height"] + 1

		self.coinbase_transaction = json.loads(transaction_to_json(coinbase_transaction(miner_public_key, miner_public_key, 0, 0, self.height)))
		self.block_reward = self.coinbase_transaction["output_amount"]

		self.total_output = self.block_reward
		self.transaction_fees = self.coinbase_transaction["fees"]

		self.merkle_root = None
		self.previous_block_hash = json_previous_block["block_hash"].encode('UTF-8')
		self.nonce = None

		self.timestamp = datetime.datetime.now() 

		self.transactions = [self.coinbase_transaction]+raw_transactions

		self.miner_public_key = miner_public_key


		def proof_of_work(self, nonce, target):
			proof = False

			while proof == False:
				encoded_nonce = str(nonce).encode('UTF-8')
				prehash_base = (self.previous_block_hash+self.merkle_root+encoded_nonce)
				test_proof = encrypt_key(prehash_base, master_key)
				if test_proof[0:len(target)] == target:
					proof = True
				else:
					nonce += 1

			self.nonce = str(nonce).encode('UTF-8')
			self.block_hash = test_proof.encode('UTF-8')

		def generate_nodes(self, transaction_pool):
			temp_list = []
			node_parent = None
			c1 = None
			c2 = None
			#print("concat layer:", layer)
			if len(transaction_pool) == 1:
				self.merkle_root = encrypt_key(json.dumps(self.coinbase_transaction).encode('UTF-8'), master_key).encode('UTF-8')
			else:
				for i in range(0, len(transaction_pool) - 1, 2):
					try:
						c1 = transaction_pool[i].encode('UTF-8')
						c2 = transaction_pool[i + 1].encode('UTF-8')
					except AttributeError:
						c1 = transaction_pool[i]
						c2 = transaction_pool[i + 1]
					try:
						node_parent = merkle_node((encrypt_key((c1 + c2), master_key)))
					except TypeError:
						node_parent = merkle_node((encrypt_key((c1.parent.encode('UTF-8') + c2.parent.encode('UTF-8')), master_key)))

					node_parent.child_left = c1
					node_parent.child_right = c2

					temp_list.append(node_parent)

				if len(temp_list) == 1:
					self.merkle_root = (temp_list[0].parent).encode('UTF-8')
				else:
					return generate_nodes(self, temp_list)

		def calculate_values(self):
			for i in raw_transactions:
				self.total_output += i["output_amount"]
				self.transaction_fees += i["fees"]

		data_list = []
		for i in self.transactions:
			data_list.append(i["transaction_data"].encode('UTF-8'))
		generate_nodes(self, data_list)
		proof_of_work(self, start_nonce, '000')
		calculate_values(self)

