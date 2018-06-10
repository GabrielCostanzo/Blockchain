import user
import pickle

from hashlib import blake2b
from hmac import compare_digest

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
"""

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

alice = user.wallet()
bob = user.wallet()
carl = user.wallet()
dave = user.wallet()

for i in range(1):
	alice.create_transaction(bob.serialized_public, 100000, 5)
	alice.create_transaction(carl.serialized_public, 10, 5)
	alice.create_transaction(bob.serialized_public, 10, 5)
	alice.create_transaction(bob.serialized_public, 100000, 5)
	alice.create_transaction(carl.serialized_public, 10, 5)
	alice.create_transaction(bob.serialized_public, 10, 5)
	
test_gen_block = chain.genesis_block(alice.serialized_public, 0)
test_reg_block = chain.block(test_gen_block, alice.pending_output_transactions, alice.serialized_public, 0)
test_reg_2_block = chain.block(test_reg_block, alice.pending_output_transactions, alice.serialized_public, 0)
test_reg_3_block = chain.block(test_reg_2_block, alice.pending_output_transactions, alice.serialized_public, 0)



#compressed_b = obj_to_compressed(test_gen_block)
import json


def insert_block(block_obj):
	json_header = json.dumps([block_obj.height, str(block_obj.block_hash.decode('UTF-8')), block_obj.total_output, block_obj.transaction_fees, str(block_obj.previous_block_hash.decode('UTF-8')), str(block_obj.merkle_root.decode('UTF-8')), str(block_obj.nonce.decode('UTF-8')), str(block_obj.timestamp)])
	print(json_header)
"""
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

one = json.loads(block_to_json(test_gen_block))
two = json.loads(block_to_json(test_reg_block))
three = json.loads(block_to_json(test_reg_2_block))
four = json.loads(block_to_json(test_reg_3_block))

#print(two)


#x = json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4, separators=(',', ': '))


#t1 = one["transactions"][0]["txid"]
#t2 = json.loads(two)["transactions"][1]["transaction_data"].encode('latin1')

#print(t1)
#print(t2)


#ver = block_verification.verify_block(two, three)
#block_verification.verify_block_transactions(compressed_block_2)
#print(ver)