from pymongo import MongoClient
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def create_connection():    
    conn = psycopg2.connect(
        database=os.environ.get('DB_NAME'), 
        user=os.environ.get('DB_USER'), 
        password=os.environ.get('DB_PASSWORD'), 
        host=os.environ.get('DB_HOST'), 
        port=os.environ.get('DB_PORT')
        )
    return conn
