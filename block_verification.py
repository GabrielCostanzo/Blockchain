import gzip 
import pickle
from chain import merkle_node
from user import encrypt_key
from user import sign 
from user import master_key
import json
from user import transaction
from chain import coinbase_transaction

def generate_merkle_root(transaction_pool):
	temp_list = []
	node_parent = None
	c1 = None
	c2 = None
	#print("concat layer:", layer)
	if len(transaction_pool) == 1:
		merkle_root = encrypt_key(transaction_pool[0], master_key).encode('UTF-8')
		return merkle_root

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
		merkle_root = (temp_list[0].parent).encode('UTF-8')
		return merkle_root
	else:
		return generate_merkle_root(temp_list)


def verify_block(json_previous_block, json_block):
	previous_block_hash = json_previous_block["block_hash"].encode('UTF-8')

	given_nonce = json_block["nonce"].encode('UTF-8')
	given_transactions = json_block["transactions"]

	transaction_list = []
	for i in given_transactions:
		good_transaction = verify_block_transactions(given_transactions[3])
		if good_transaction == True:
			transaction_list.append(i["transaction_data"])
		else:
			return False

	target_merkle_root = generate_merkle_root(transaction_list)
	target_height = (json_previous_block["height"]) + 1
	target_zeros  = '00000'
	target_hash_base = previous_block_hash+target_merkle_root+given_nonce
	target_hash = encrypt_key(target_hash_base, master_key).encode('UTF-8')

	confirmation_list = [False, False, False, False]

	if json_block["merkle_root"].encode('UTF-8') == target_merkle_root:
		confirmation_list[0] = True
	if target_height == json_block["height"]:
		confirmation_list[1] = True

	zero_count = 0 
	for i in range(len(target_zeros)):
		if json_block["block_hash"][i] == '0':
			zero_count += 1

	if zero_count == len(target_zeros):
		confirmation_list[2] = True

	if target_hash == json_block["block_hash"].encode('UTF-8'):
		confirmation_list[3] = True

	if False in confirmation_list:
		return False
	else:
		return True


def verify_block_transactions(transaction):
	print(json.dumps(transaction, sort_keys=False, indent=4, separators=(',', ': ')))
	transaction_obj = (pickle.loads(transaction["transaction_data"].encode('latin1')))
	
	coinbase_required_depth = 100
	correct_obj = False
	correct_sig = False
	included_sig = False

	if isinstance(transaction_obj, coinbase_transaction) or isinstance(transaction_obj, coinbase_transaction):
		correct_obj = True
	else: 
		correct_obj = False

	print(transaction_obj.sender_sig)
	#print(transaction_obj.transaction_data)
	print(transaction_obj.sender_public_key)
	print(transaction_obj.receiver_public_key)
	print(transaction_obj.input_amount)
	print(transaction_obj.fees)
	print(transaction_obj.output_amount)
	print(transaction_obj.input_transactions)
	print(transaction_obj.status)
	print(transaction_obj.txid)
	print(transaction_obj.timestamp)
