import user
import pickle
from wallet_log import user_login
from wallet_log import loaded_wallet
from hashlib import blake2b
from hmac import compare_digest
import pymongo
import json


from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

import chain
import block_verification

import gzip
import pymysql

from json_serialize import block_to_json
from json_serialize import transaction_to_json

def print_block(block_object):
	print("GEN_BLOCK:\n\n\n")
	print("\nblock hash:")
	print(block_object.block_hash)
	print("\nprevious block hash:")
	print(block_object.previous_block_hash)
	print("\nmerkle root:")
	print(block_object.merkle_root)
	print("\nnonce:")
	print(block_object.nonce)
	print("\ncoinbase transaction:")
	print(block_object.coinbase_transaction)
	print("\ntransaction fees:")
	print(block_object.transaction_fees)
	print("\nblock reward:")
	print(block_object.block_reward)
	print("\ntotal output:")
	print(block_object.total_output)
	print("\nblock height:")
	print(block_object.height)
	print("\ntimestamp:")
	print(block_object.timestamp)
	print("\ntransactions:")
	print(block_object.transactions)
	print("\nminer public key:")
	print(block_object.miner_public_key)
	print("\n")
"""
def save_block(block):
	height = block.height
	pick_block = pickle.dumps(block)
	with open('test.txt', 'wb') as f:
		f.write((pick_block))

def obj_to_compressed(obj):
	pickled_block = pickle.dumps(obj)
	compressed = gzip.compress(pickled_block)
	return compressed

def compressed_to_obj(compressed):
	decompressed = gzip.decompressed(compressed)
	obj = pickle.loads(decompressed)
	return obj

def record_inputs():
	pass

def update_chain_point():
	#access save point
	try:
		with open("chain_point.txt", "r") as chain_point_file:
			block_point = int(chain_point_file.read())
	except FileNotFoundError:
		with open("chain_point.txt", "w") as chain_point_file:
			block_point = 0
			chain_point_file.write(str(block_point))
	#request blocks above and equal to savepoint from full nodes
	#search chain for inputs
	#update wallet with inputs 
	#archive new save point
	print(block_point)
"""

#Establish connection to the database
#connection_one = pymysql.connect(host='localhost', port=3306, user='root', passwd='1Gia2Harley',
# db='blockchain', autocommit = True)
#Create cursors to interact with the databases
#cur_1 = connection_one.cursor()
#cur_1.execute("INSERT INTO PRE_FLOP_TBL VALUES ('%s', '%s')"%(float(botoplist[-1])*.01,  float(botopgroups[-1])*.01))
"""
cur_1.execute("SELECT * FROM BLOCK_TBL")
for i in cur_1:
	print(pickle.loads(i[1]).block_hash)
"""

"""
def insert_block(block_obj):
	json_header = json.dumps([block_obj.height, str(block_obj.block_hash.decode('UTF-8')), block_obj.total_output, block_obj.transaction_fees, str(block_obj.previous_block_hash.decode('UTF-8')), str(block_obj.merkle_root.decode('UTF-8')), str(block_obj.nonce.decode('UTF-8')), str(block_obj.timestamp)])
	print(json_header)

	pickled = pickle.dumps(block_obj)
	print(pickled)
	print("\n\n\n")
	print(type(pickled))
	print(type(b"test"))
	print(str(pickled, 'utf-8'))
	#cur_1.execute("INSERT INTO HEADER_TBL VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(block_obj.height, block_obj.block_hash, block_obj.total_output, block_obj.transaction_fees, block_obj.previous_block_hash, block_obj.merkle_root, block_obj.nonce, block_obj.timestamp))
	cur_1.execute("INSERT INTO BLOCK_TBL VALUES ('%s', '%s')"%(6, pickled))
"""

"""
	print("\nheader_tbl data:")
	print(block_obj.height)
	print(block_obj.block_hash)
	print(block_obj.total_output)
	print(block_obj.transaction_fees)
	print(block_obj.previous_block_hash)
	print(block_obj.merkle_root)
	print(block_obj.nonce)
	print(block_obj.timestamp)
"""


#genesis_to_json(test_gen_block)

#print((block_to_json(test_reg_block)))

#x = json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4, separators=(',', ': '))


#t1 = one["transactions"][0]["txid"]
#t2 = json.loads(two)["transactions"][1]["transaction_data"].encode('latin1')

#print(t1)
#print(t2)


#ver = block_verification.verify_block(two, three)
#block_verification.verify_block_transactions(compressed_block_2)
#print(ver)

client = pymongo.MongoClient()
db = client.database

#collection named posts:
blocks = db.blocks
utxo_pool = db.utxo_pool

#posts.insert_one(block_o)
#posts.insert_one(block_tw)

#single = posts.find_one({"author": "Mike"})

#remove all:
#posts.remove({})


alice = user.wallet()
bob = user.wallet()
tim = user.wallet()
zach = user.wallet()
carl = user.wallet()
dave = user.wallet()
gabe = loaded_wallet(user_login()) 

	
#test_gen_block = chain.genesis_block(gabe.serialized_public, 0)
#test_reg_block = chain.block(test_gen_block, gabe.pending_output_transactions, gabe.serialized_public, 0)
#test_reg_2_block = chain.block(test_reg_block, gabe.pending_output_transactions, gabe.serialized_public, 0)
#test_reg_3_block = chain.block(test_reg_2_block, gabe.pending_output_transactions, gabe.serialized_public, 0)

#zero = json.loads(block_to_json(test_gen_block))
#one = json.loads(block_to_json(test_reg_block))
#two = json.loads(block_to_json(test_reg_2_block))
#three = json.loads(block_to_json(test_reg_3_block))

#blocks.insert_one(zero)
#blocks.remove({})

"""
def mine(prev_block):
	if blocks.find_one({"_id": 0}) == None:
		block = chain.genesis_block(gabe.serialized_public, 0)
		blocks.insert_one(json.loads(block_to_json(block)))
		print(blocks.count())
	else:
		block = chain.block(prev_block, gabe.pending_output_transactions, gabe.serialized_public, 0)
		blocks.insert_one(json.loads(block_to_json(block)))
		print(blocks.count())

	return mine(block)
"""

#blocks.insert_one(json.loads(block_to_json(test_gen_block)))

#mine(test_gen_block)

#print(blocks.count())

import pprint
import time 

def gather_coinbase_inputs():
	for i in range(0, blocks.count()):
		current = blocks.find_one({"_id": i})
		for j in current["transactions"]:
			if (j["receiver_public_key"].encode('UTF-8') == gabe.serialized_public):
				print([j["txid"], j["output_amount"], j["status"]])


#print(gabe.unspent_input_transactions)
#gabe.update_input_transactions()


#pprint.pprint(json.loads(transaction_to_json(x)))


#print(gabe.unspent_input_transactions)
#gather_coinbase_inputs()
#print(blocks.find_one({"_id": 0})["transactions"])

gabe.create_transaction(tim.serialized_public, 20, 5.4)
gabe.create_transaction(zach.serialized_public, 10, 8.8)
gabe.create_transaction(carl.serialized_public, 15, 4.2)
gabe.create_transaction(dave.serialized_public, 22, 21)

gabe.create_transaction(tim.serialized_public, 11.5, 0)
gabe.create_transaction(zach.serialized_public, 6, 5)

gabe.create_transaction(carl.serialized_public, 16, 4)


#print("unspent:")
#print(gabe.unspent_input_transactions)
#print("\nspent:")
#print(gabe.spent_input_transactions)

#test_gen_block = chain.genesis_block(gabe.serialized_public, 0)
#test_reg_block = chain.block(test_gen_block, gabe.pending_output_transactions, gabe.serialized_public, 0)
#test_reg_2_block = chain.block(test_reg_block, gabe.pending_output_transactions, gabe.serialized_public, 0)
#test_reg_3_block = chain.block(test_reg_2_block, gabe.pending_output_transactions, gabe.serialized_public, 0)

#zero = json.loads(block_to_json(test_gen_block))
#one = json.loads(block_to_json(test_reg_block))
#two = json.loads(block_to_json(test_reg_2_block))
#three = json.loads(block_to_json(test_reg_3_block))


#pprint.pprint(one)

#ver = block_verification.verify_block(two, three)
#for i in one["transactions"]:
	#block_verification.verify_block_transactions(i)
#print(ver)

#mempool = gabe.pending_output_transactions
mempool = []

def perpet_mine(prev_block):
	block = chain.block(prev_block, mempool, gabe.serialized_public, 0)
	ver = block_verification.verify_block(prev_block, block)
	if ver == True:
		blocks.insert_one(json.loads(block_to_json(block)))
		print("block added !")
		print(blocks.count())
		return perpet_mine(json.loads(block_to_json(block)))
	else:
		print ("block addition failed")
		return


def init_mine():
	if blocks.find_one({"_id": 0}) == None:
		block = chain.genesis_block(gabe.serialized_public, 0)
		blocks.insert_one(json.loads(block_to_json(block)))
		print(blocks.count())

	else:
		print(blocks.count())
		block_count = blocks.count()
		last_block = blocks.find_one({"_id": block_count - 1})
		perpet_mine(last_block)

init_mine()



"""
last_block = blocks.find_one({"_id": 39})
block = chain.block(last_block, gabe.pending_output_transactions, gabe.serialized_public, 0)

ver = block_verification.verify_block(last_block, block)
print(ver)
#print(blocks.count())

	else:
		block = chain.block(prev_block, gabe.pending_output_transactions, gabe.serialized_public, 0)
		blocks.insert_one(json.loads(block_to_json(block)))
		print(blocks.count())
"""
#pprint.pprint(blocks.find_one({"_id": 75}))