from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/", connect=False)

db = client.get_database("secrets_db")
secrets_collection = db.get_collection("secrets")

if "secrets" not in db.list_collection_names():
    db.create_collection("secrets")

client.server_info()
