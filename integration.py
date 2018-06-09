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
connection_one = pymysql.connect(host='localhost', port=3306, user='root', passwd='1Gia2Harley',
 db='blockchain', autocommit = True)
#Create cursors to interact with the databases
cur_1 = connection_one.cursor()
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
	alice.create_transaction(carl.serialized_public, 500, 50)
	alice.create_transaction(bob.serialized_public, 10, 5)
	alice.create_transaction(carl.serialized_public, 90000, 5)
	alice.create_transaction(bob.serialized_public, 10000000, 600)
	alice.create_transaction(carl.serialized_public, 10, 3)
	alice.create_transaction(bob.serialized_public, 10, 5)
	alice.create_transaction(carl.serialized_public, 10, 5)

test_gen_block = chain.genesis_block(alice.serialized_public, 0)
test_reg_block = chain.block(test_gen_block, alice.pending_output_transactions, alice.serialized_public, 0)
test_reg_2_block = chain.block(test_reg_block, alice.pending_output_transactions, alice.serialized_public, 0)
test_reg_3_block = chain.block(test_reg_2_block, alice.pending_output_transactions, alice.serialized_public, 0)


#ver = block_verification.verify_block(compressed_block_2, compressed_block_3)
#block_verification.verify_block_transactions(compressed_block_2)

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
def transaction_to_json(transaction_obj):

	if transaction_obj.status == "coinbase":
		print(json.dumps({"sender_sig": transaction_obj.sender_sig, "transaction_data": transaction_obj.transaction_data,
		"sender_public_key": transaction_obj.sender_public_key.decode('UTF-8'), "receiver_public_key": transaction_obj.receiver_public_key.decode('UTF-8'), "input_amount": transaction_obj.input_amount, "fees": transaction_obj.fees,
		"output_amount": transaction_obj.output_amount, "input_transactions": transaction_obj.input_transactions, "status": transaction_obj.status, "txid": transaction_obj.txid, "timestamp": str(transaction_obj.timestamp)},
		sort_keys=True, indent=4, separators=(',', ': ')))

		json_transaction = json.dumps({"sender_sig": transaction_obj.sender_sig, "transaction_data": transaction_obj.transaction_data,
		"sender_public_key": transaction_obj.sender_public_key.decode('UTF-8'), "receiver_public_key": transaction_obj.receiver_public_key.decode('UTF-8'), "input_amount": transaction_obj.input_amount, "fees": transaction_obj.fees,
		"output_amount": transaction_obj.output_amount, "input_transactions": transaction_obj.input_transactions, "status": transaction_obj.status, "txid": transaction_obj.txid, "timestamp": str(transaction_obj.timestamp)})
	else:
		print(json.dumps({"sender_sig": transaction_obj.sender_sig.decode('latin1'),  "transaction_data": transaction_obj.transaction_data.decode('latin1'),
		"sender_public_key": transaction_obj.sender_public_key.decode('UTF-8'), "receiver_public_key": transaction_obj.receiver_public_key.decode('UTF-8'), "input_amount": transaction_obj.input_amount, "fees": transaction_obj.fees,
		"output_amount": transaction_obj.output_amount, "input_transactions": transaction_obj.input_transactions, "status": transaction_obj.status, "txid": transaction_obj.txid.decode('UTF-8'), "timestamp": str(transaction_obj.timestamp)},
		sort_keys=True, indent=4, separators=(',', ': ')))

		json_transaction = json.dumps({"sender_sig": transaction_obj.sender_sig.decode('latin1'),  "transaction_data": transaction_obj.transaction_data.decode('latin1'),
		"sender_public_key": transaction_obj.sender_public_key.decode('UTF-8'), "receiver_public_key": transaction_obj.receiver_public_key.decode('UTF-8'), "input_amount": transaction_obj.input_amount, "fees": transaction_obj.fees,
		"output_amount": transaction_obj.output_amount, "input_transactions": transaction_obj.input_transactions, "status": transaction_obj.status, "txid": transaction_obj.txid.decode('UTF-8'), "timestamp": str(transaction_obj.timestamp)},
		sort_keys=True, indent=4, separators=(',', ': '))
		
	return json_transaction

"""
def genesis_to_json(block_obj):
	coinbase = pickle.loads(block_obj.coinbase_transaction)
	coinbase_json = transaction_to_json(coinbase)
	print(json.dumps({"block_hash": block_obj.block_hash.decode('UTF-8'), "height": block_obj.height,
	"coinbase_transaction": json.loads(coinbase_json), 
	"transaction_fees": block_obj.transaction_fees, "block_reward": block_obj.block_reward, "total_output": block_obj.total_output,
	"previous_block_hash": block_obj.previous_block_hash.decode('UTF-8'), "merkle_root": block_obj.merkle_root.decode('UTF-8'),
	"nonce": block_obj.nonce.decode('UTF-8'), "timestamp": str(block_obj.timestamp), "transactions": json.loads(coinbase_json), "miner_public_key": block_obj.miner_public_key.decode('UTF-8')},
	sort_keys=True, indent=4, separators=(',', ': ')))
"""

def block_to_json(block_obj):
	coinbase = pickle.loads(block_obj.coinbase_transaction)
	coinbase_json = transaction_to_json(coinbase)
	json_transactions = []

	for i in block_obj.transactions:
		t_obj = pickle.loads(i)
		json_transactions.append(json.loads(transaction_to_json(t_obj)))
	print("RUN:\n\n\n")
	print(json.dumps({"block_hash": block_obj.block_hash.decode('UTF-8'), "height": block_obj.height,
	"coinbase_transaction": json.loads(coinbase_json), 
	"transaction_fees": block_obj.transaction_fees, "block_reward": block_obj.block_reward, "total_output": block_obj.total_output,
	"previous_block_hash": block_obj.previous_block_hash.decode('UTF-8'), "merkle_root": block_obj.merkle_root.decode('UTF-8'),
	"nonce": block_obj.nonce.decode('UTF-8'), "timestamp": str(block_obj.timestamp), "transactions": json_transactions, "miner_public_key": block_obj.miner_public_key.decode('UTF-8')},
	sort_keys=True, indent=4, separators=(',', ': ')))

#genesis_to_json(test_gen_block)
block_to_json(test_gen_block)
block_to_json(test_reg_block)
block_to_json(test_reg_2_block)
block_to_json(test_reg_3_block)
