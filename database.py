from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    client = MongoClient(os.environ.get('MONDODB_URI'))
    return client
