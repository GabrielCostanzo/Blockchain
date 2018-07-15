import json

def transaction_to_json(transaction_obj):

	if transaction_obj.status == "coinbase":
		json_transaction = json.dumps({"sender_sig": transaction_obj.sender_sig, "transaction_data": transaction_obj.transaction_data,
		"sender_public_key": transaction_obj.sender_public_key.decode('UTF-8'), "receiver_public_key": transaction_obj.receiver_public_key.decode('UTF-8'), "input_amount": transaction_obj.input_amount, "fees": transaction_obj.fees,
		"output_amount": transaction_obj.output_amount, "input_transactions": transaction_obj.input_transactions, "status": transaction_obj.status, "txid": transaction_obj.txid.decode('UTF-8'), "timestamp": str(transaction_obj.timestamp)},
		sort_keys=False, indent=4, separators=(',', ': '))
	else:
		json_transaction = json.dumps({"sender_sig": transaction_obj.sender_sig.decode('latin1'),  "transaction_data": transaction_obj.transaction_data,
		"sender_public_key": transaction_obj.sender_public_key.decode('UTF-8'), "receiver_public_key": transaction_obj.receiver_public_key.decode('UTF-8'), "input_amount": transaction_obj.input_amount, "fees": transaction_obj.fees,
		"output_amount": transaction_obj.output_amount, "input_transactions": transaction_obj.input_transactions, "status": transaction_obj.status, "txid": transaction_obj.txid.decode('UTF-8'), "timestamp": str(transaction_obj.timestamp)},
		sort_keys=False, indent=4, separators=(',', ': '))
		
	return json_transaction

def block_to_json(block_obj):
	json_obj = json.dumps({"_id": block_obj.height, "block_hash": block_obj.block_hash.decode('UTF-8'), "height": block_obj.height,
	"coinbase_transaction": block_obj.coinbase_transaction, 
	"transaction_fees": block_obj.transaction_fees, "block_reward": block_obj.block_reward, "total_output": block_obj.total_output,
	"previous_block_hash": block_obj.previous_block_hash.decode('UTF-8'), "merkle_root": block_obj.merkle_root.decode('UTF-8'),
	"nonce": block_obj.nonce.decode('UTF-8'), "timestamp": str(block_obj.timestamp), "transactions": block_obj.transactions, "miner_public_key": block_obj.miner_public_key.decode('UTF-8')},
	sort_keys=False, indent=4, separators=(',', ': '))

	return json_obj

def wallet_to_json(wallet_obj):
	json_wallet = json.dumps({"serialized_private": wallet_obj.serialized_private.decode('UTF-8'),
		"serialized_public": wallet_obj.serialized_public.decode('UTF-8'), "pending_output_transactions": wallet_obj.pending_output_transactions,
		"confirmed_output_transactions": wallet_obj.confirmed_output_transactions, "unspent_input_transactions": wallet_obj.unspent_input_transactions,
		"spent_input_transactions": wallet_obj.spent_input_transactions})
	return json_wallet
