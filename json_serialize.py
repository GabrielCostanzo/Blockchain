def transaction_to_json(transaction_obj):

	if transaction_obj.status == "coinbase":
		"""
		print(json.dumps({"sender_sig": transaction_obj.sender_sig, "transaction_data": transaction_obj.transaction_data,
		"sender_public_key": transaction_obj.sender_public_key.decode('UTF-8'), "receiver_public_key": transaction_obj.receiver_public_key.decode('UTF-8'), "input_amount": transaction_obj.input_amount, "fees": transaction_obj.fees,
		"output_amount": transaction_obj.output_amount, "input_transactions": transaction_obj.input_transactions, "status": transaction_obj.status, "txid": transaction_obj.txid, "timestamp": str(transaction_obj.timestamp)},
		sort_keys=True, indent=4, separators=(',', ': ')))
		"""

		json_transaction = json.dumps({"sender_sig": transaction_obj.sender_sig, "transaction_data": transaction_obj.transaction_data,
		"sender_public_key": transaction_obj.sender_public_key.decode('UTF-8'), "receiver_public_key": transaction_obj.receiver_public_key.decode('UTF-8'), "input_amount": transaction_obj.input_amount, "fees": transaction_obj.fees,
		"output_amount": transaction_obj.output_amount, "input_transactions": transaction_obj.input_transactions, "status": transaction_obj.status, "txid": transaction_obj.txid, "timestamp": str(transaction_obj.timestamp)},
		sort_keys=False, indent=4, separators=(',', ': '))
	else:
		"""
		print(json.dumps({"sender_sig": transaction_obj.sender_sig.decode('latin1'),  "transaction_data": transaction_obj.transaction_data.decode('latin1'),
		"sender_public_key": transaction_obj.sender_public_key.decode('UTF-8'), "receiver_public_key": transaction_obj.receiver_public_key.decode('UTF-8'), "input_amount": transaction_obj.input_amount, "fees": transaction_obj.fees,
		"output_amount": transaction_obj.output_amount, "input_transactions": transaction_obj.input_transactions, "status": transaction_obj.status, "txid": transaction_obj.txid.decode('UTF-8'), "timestamp": str(transaction_obj.timestamp)},
		sort_keys=True, indent=4, separators=(',', ': ')))
		"""

		json_transaction = json.dumps({"sender_sig": transaction_obj.sender_sig.decode('latin1'),  "transaction_data": transaction_obj.transaction_data.decode('latin1'),
		"sender_public_key": transaction_obj.sender_public_key.decode('UTF-8'), "receiver_public_key": transaction_obj.receiver_public_key.decode('UTF-8'), "input_amount": transaction_obj.input_amount, "fees": transaction_obj.fees,
		"output_amount": transaction_obj.output_amount, "input_transactions": transaction_obj.input_transactions, "status": transaction_obj.status, "txid": transaction_obj.txid.decode('UTF-8'), "timestamp": str(transaction_obj.timestamp)},
		sort_keys=False, indent=4, separators=(',', ': '))
		
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

	"""
	print(json.dumps({"block_hash": block_obj.block_hash.decode('UTF-8'), "height": block_obj.height,
	"coinbase_transaction": json.loads(coinbase_json), 
	"transaction_fees": block_obj.transaction_fees, "block_reward": block_obj.block_reward, "total_output": block_obj.total_output,
	"previous_block_hash": block_obj.previous_block_hash.decode('UTF-8'), "merkle_root": block_obj.merkle_root.decode('UTF-8'),
	"nonce": block_obj.nonce.decode('UTF-8'), "timestamp": str(block_obj.timestamp), "transactions": json_transactions, "miner_public_key": block_obj.miner_public_key.decode('UTF-8')},
	sort_keys=True, indent=4, separators=(',', ': ')))
	"""

	json_obj = json.dumps({"block_hash": block_obj.block_hash.decode('UTF-8'), "height": block_obj.height,
	"coinbase_transaction": json.loads(coinbase_json), 
	"transaction_fees": block_obj.transaction_fees, "block_reward": block_obj.block_reward, "total_output": block_obj.total_output,
	"previous_block_hash": block_obj.previous_block_hash.decode('UTF-8'), "merkle_root": block_obj.merkle_root.decode('UTF-8'),
	"nonce": block_obj.nonce.decode('UTF-8'), "timestamp": str(block_obj.timestamp), "transactions": json_transactions, "miner_public_key": block_obj.miner_public_key.decode('UTF-8')},
	sort_keys=False, indent=4, separators=(',', ': '))

	return json_obj

