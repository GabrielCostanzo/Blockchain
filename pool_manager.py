import pymongo

client = pymongo.MongoClient()
db = client.database

blocks = db.blocks
utxo_pool = db.utxo_pool

def update_utxo_pool_single(input_json_b):
	for j in input_json_b["transactions"]:
		if j["status"] != "coinbase":
			for n in j["input_transactions"]:
				utxo_pool.remove({"_id": n[0]})
		try:
			utxo_pool.insert_one({"_id": j["txid"], "value": j["output_amount"]})
		except:
			pass

	
def update_utxo_pool_full():
	for i in range(0, blocks.count()):
		current = blocks.find_one({"_id": i})
		if current != None:	
			update_utxo_pool_single(current)