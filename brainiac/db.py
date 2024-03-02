from pymongo import MongoClient
from flask import current_app

MONGO_URI = current_app.config['MONGO_URI']

client = MongoClient(MONGO_URI)

db = client.brainiac_db