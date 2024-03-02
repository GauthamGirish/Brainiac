from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI)

db = client.brainiac_db
