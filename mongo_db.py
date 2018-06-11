import pymongo
import json
import pprint
import integration

client = pymongo.MongoClient()
db = client.test_database
collection = db.test_collection

#all posts:
posts = db.posts

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

all_blocks = posts.find({})
for i in all_blocks:
	print("\n\n\n\n\n\n")
	pprint.pprint(i)