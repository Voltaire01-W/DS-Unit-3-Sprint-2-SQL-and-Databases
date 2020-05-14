import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

DB_USER = os.getenv("MONGO_USER", default="OOPS")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")

connection_uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}.mongodb.net/test?retryWrites=true&w=majority"

# client = pymongo.MongoClient("mongodb://Voltaire22:<password>@assignments-shard-00-00-xo7n0.gcp.mongodb.net:27017,assignments-shard-00-01-xo7n0.gcp.mongodb.net:27017,assignments-shard-00-02-xo7n0.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Assignments-shard-0&authSource=admin&retryWrites=true&w=majority")

client = pymongo.MongoClient(connection_uri)

db = client.test_database

collection = db.rpg

path = os.path.join(os.path.dirname(__file__), "..", "module3-nosql-and-document-oriented-databases", "testdata.json")

with open(path) as f:
    file_data = json.load(f)

collection.insert_many(file_data)

result = collection.count_documents({"model":"charactercreator.character"})
print("There are", result, "total characters.")
result2 = collection.count_documents({"model":"charactercreator.cleric"})
print("There are", result2, "clerics.")
result2 = collection.count_documents({"model":"charactercreator.fighter"})
print("There are", result2, "fighters.")
result2 = collection.count_documents({"model":"charactercreator.mage"})
print("There are", result2, "mages.")
result2 = collection.count_documents({"model":"charactercreator.necromancer"})
print("There are", result2, "necromancers.")
result2 = collection.count_documents({"model":"charactercreator.thief"})
print("There are", result2, "thieves.")
items = collection.count_documents({"model":"armory.item"})
print("There are", items, "total items.")
weapons = collection.count_documents({"model":"armory.weapon"})
print("There are", weapons, "items that are weapons.")
nonweapons = items - weapons
print("There are", nonweapons, "items that are not weapons.")