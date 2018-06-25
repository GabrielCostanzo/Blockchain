import gzip 
import pickle
from chain import merkle_node
from user import encrypt_key
from user import sign 
from user import master_key
import json
from user import transaction as t_obj
from chain import coinbase_transaction
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from pool_manager import update_utxo_pool_single
from pool_manager import  update_utxo_pool_full
import pymongo

client = pymongo.MongoClient()
db = client.database

#collection named posts:
blocks = db.blocks
utxo_pool = db.utxo_pool

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
	update_utxo_pool_full()
	previous_block_hash = json_previous_block["block_hash"].encode('UTF-8')

	given_nonce = json_block["nonce"].encode('UTF-8')
	given_transactions = json_block["transactions"]

	spent_inputs = []

	transaction_list = []
	for i in given_transactions:
		good_transaction = verify_block_transactions(i)
		if good_transaction[0] == True:
			transaction_list.append(i["transaction_data"])
			spent_inputs = good_transaction[1]
			for i in spent_inputs:
				utxo_pool.remove({"_id": i["_id"]})
			spent_inputs = []
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
	#print(json.dumps(transaction, sort_keys=False, indent=4, separators=(',', ': ')))
	used_transactions = []
	transaction_obj = (pickle.loads(transaction["transaction_data"].encode('latin1')))

	correct_obj = False
	correct_sig = True
	valid_value = True
	correct_value = True
	correct_match = True
	valid_input_value = True
	running_input_value = 0 

	transaction_data = transaction["transaction_data"].encode('latin1')
	serial_pub = (transaction["sender_public_key"].encode('UTF-8'))
	public_key_obj = serialization.load_pem_public_key(serial_pub, backend=default_backend())

	json_input_amount = transaction["input_amount"]
	json_output_amount = transaction["output_amount"]
	json_fees = transaction["fees"]

	obj_input_amount = transaction_obj.input_amount
	obj_output_amount = transaction_obj.output_amount
	obj_fees = transaction_obj.fees

	if isinstance(transaction_obj, coinbase_transaction) or isinstance(transaction_obj, t_obj):
		correct_obj = True

	if transaction["status"] == "Signed":
		sig = transaction["sender_sig"].encode('latin1')
		if (public_key_obj.verify(sig, transaction_data, ec.ECDSA(hashes.SHA256())) != True):
			correct_sig = False

		if (json_input_amount - json_fees) != json_output_amount:
			correct_value = False
		if (obj_input_amount - obj_fees) != obj_output_amount:
			correct_value = False

		for i in transaction["input_transactions"]:
			mongo_input_transaction = utxo_pool.find_one({"_id": i[0]})

			if mongo_input_transaction == None or mongo_input_transaction in used_transactions:
				valid_input_value = False
			else:
				running_input_value += mongo_input_transaction["value"]
				used_transactions.append(mongo_input_transaction)

		if running_input_value < transaction["input_amount"]:
			valid_input_value = False


	if (json_input_amount - json_fees) < 0:
		valid_value = False
	if (obj_input_amount - obj_fees) < 0:
		valid_value = False

	if transaction_obj.sender_public_key != transaction["sender_public_key"].encode('UTF-8'):
		correct_match = False

	if transaction_obj.receiver_public_key != transaction["receiver_public_key"].encode('UTF-8'):
		correct_match = False

	if transaction_obj.input_amount != transaction["input_amount"]:
		correct_match = False

	if transaction_obj.fees != transaction["fees"]:
		correct_match = False

	if transaction_obj.output_amount != transaction["output_amount"] and transaction["status"] != "coinbase":
		correct_match = False

	if transaction_obj.input_transactions != transaction["input_transactions"]:
		correct_match = False

	if str(transaction_obj.timestamp) != transaction["timestamp"]:
		correct_match = False

	validity_list = [correct_obj, correct_sig, valid_value, correct_value, correct_match, valid_input_value]

	if False in validity_list:
		return [False, None]
	else:
		return [True, used_transactions]



