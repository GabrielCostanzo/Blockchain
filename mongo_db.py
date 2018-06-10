import pymongo

client = pymongo.MongoClient()
db = client.test_database
collection = db.test_collection

import datetime
#post = {"author": "Mike","text": "My first blog post!",
#"tags": ["mongodb", "python", "pymongo"],"date": datetime.datetime.utcnow()}

posts = db.posts
#post_id = posts.insert_one(post).inserted_id

#print(post_id)

#print(db.collection_names(include_system_collections=False))


#x = posts.find_one({"author": "Mike"})
#print(x)

#import integration
#import json

#block = integration.two

#print(json.dumps(block))

#print(block)

#import pprint

#print("\n\n\n\n\n\n\n\n")
#pprint.pprint(block)

#block_post = posts.insert_one(block).inserted_id

#x = posts.find_one({"block_reward": 50})

#pprint.pprint(x)