from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    client = MongoClient(os.environ.get('MONGODB_URI'))
    return client
