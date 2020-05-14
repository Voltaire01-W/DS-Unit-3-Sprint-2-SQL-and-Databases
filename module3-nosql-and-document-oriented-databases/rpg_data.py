import pymongo
import os
from dotenv import load_dotenv
import json
# import sqlite3

# client = pymongo.MongoClient("mongodb+srv://Voltaire22:<password>@assignments-xo7n0.gcp.mongodb.net/test?retryWrites=true&w=majority")
# db = client.test


load_dotenv()

DB_USER = os.getenv("MONGO_USER", default="OOPS")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")

connection_uri = f"mongodb://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}.mongodb.net/test?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_uri)
print("----------------")
print("CLIENT:", type(client), client)

db = client.test_database # "test_database" or whatever you want to call it
print("----------------")
print("DB:", type(db), db)

collection = db.rpg_test # "pokemon_test" or whatever you want to call it
print("----------------")
print("COLLECTION:", type(collection), collection)


# armory_items = pd.DataFrame(lite_tlist, columns = ['item_id', 'name', 'value', 'weight'])

path = os.path.join(os.path.dirname(__file__), 'testdata.json')

records = json.loads(path) #.values()
db.collection.insert_one(records)
print(db.list_collection_names())

# lite_tlist = [list(x) for x in lite_obj]
