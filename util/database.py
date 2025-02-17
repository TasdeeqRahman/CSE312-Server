import json
import sys
import os

from pymongo import MongoClient

docker_db = os.environ.get('DOCKER_DB', "false")

if docker_db == "true":
    print("using docker compose db")
    mongo_client = MongoClient("mongo")
else:
    print("using local db")
    mongo_client = MongoClient("localhost")

# cse312 database
db = mongo_client["cse312"]

# chat collection in cse312 database (empty for now)
chat_collection = db["chat"]

#######################

