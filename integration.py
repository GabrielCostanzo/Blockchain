import user
import pickle

from hashlib import blake2b
from hmac import compare_digest

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

import chain


import gzip

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


#with open("blockchain.txt", "wb") as file:
#	file.write(pickled_block)

def save_block(block):
	height = block.height
	pick_block = pickle.dumps(block)
	with open('%s.txt'%height, 'wb') as f:
		f.write(gzip.compress(pick_block))


#print(pickle.loads(y).block_hash)


import block_verification
"""
pickled_block_2 = (pickle.dumps(test_reg_2_block))
pickled_block_3 = (pickle.dumps(test_reg_3_block))

compressed_block_2 = gzip.compress(pickled_block_2)
compressed_block_3 = gzip.compress(pickled_block_3)

ver = block_verification.verify_block(compressed_block_2, compressed_block_3)

block_verification.verify_block_transactions(compressed_block_2)
"""


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


save_block(test_gen_block)
save_block(test_reg_block)
save_block(test_reg_2_block)
save_block(test_reg_3_block)
#update_chain_point()

print_block(test_reg_2_block)


