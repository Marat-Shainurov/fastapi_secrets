import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv('CLIENT_ADDRESS_AND_PORT'), connect=False)

db = client.get_database("secrets_db")
secrets_collection = db.get_collection("secrets")

if "secrets" not in db.list_collection_names():
    db.create_collection("secrets")

client.server_info()
