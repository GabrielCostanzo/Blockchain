import pymongo
import json
import pprint
import integration

client = pymongo.MongoClient()
db = client.test_database
collection = db.test_collection

#collection named posts:
posts = db.posts

inputs = db.inputs

#post id:
#post_id = posts.insert_one(post).inserted_id

#find:
#single = posts.find_one({"author": "Mike"})
#all = posts.find({})

#integration testing:
#block_o = integration.one
#block_tw = integration.two
#pprint.pprint(json.dumps(block))
#print(block)
#pprint.pprint(block)

#posts.insert_one(block_o)
#posts.insert_one(block_tw)

#remove all:
#posts.remove({})

#count posts:
#print(posts.count())

inputs.remove({})

"""
all_blocks = posts.find({})
for i in all_blocks:
	print("\n\n\n\n\n\n")
	pprint.pprint(i)

with open("test_json_block.json", "w") as json_file:
	json.dump(block_tw, json_file)
"""

#posts.insert_one({})

"""
print("unspent:")
count = 0
for i in integration.gabe.unspent_input_transactions:
	print(i, count)
	count += 1
	inputs.insert_one({"_id": i[0], "value": i[1]})

print("\nspent:")
for i in integration.gabe.spent_input_transactions:
	print(i)
#print("\nspent:")
#print(gabe.spent_input_transactions)

x = inputs.find({"value": 50})
for i in x:
	print(i)
"""