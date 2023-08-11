import datetime
import pprint

import pymongo as pyM

client = pyM.MongoClient("mongodb+srv://leonardoscatolin20:palmeiras@teste.8ucuvlb.mongodb.net/?retryWrites=true&w=majority")

db = client.test
collection = db.test_collection
print(db.test_collection)

post = {
    "author": "Mike",
    "text": "My First MongoDB application based on python",
    "tags": ["mongodb", "python", "pymongo"],
    "data": datetime.datetime.utcnow()
}

posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)

#print(db.posts.find_one())

pprint.pprint(db.posts.find_one())

# bulk inserts
new_posts = [{
        "author": "Mike",
        "text": "Another post",
        "tags": ["bulk", "post", "insert"],
        "date": datetime.datetime.utcnow()
        },
    {
        "author": "Leo",
        "text": "Palmeiras",
        "title": "Maior campeão do Brasil",
        "tags": ["time", "seleção", "abel"],
        "date": datetime.datetime.utcnow()
    }]

result = posts.insert_many(new_posts)
print(result.inserted_ids)

print("\nRecuperação final")
pprint.pprint(db.posts.find_one({"author": "Leo"}))

print("\n Documentos presentes na coleção posts")
for post in posts.find():
    pprint.pprint(post)
