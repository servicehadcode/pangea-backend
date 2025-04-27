from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # To load environment variables from a .env file

def get_mongo_db():
    """
    This function connects to the MongoDB database using credentials stored in environment variables
    and returns the database instance.
    """
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # Default MongoDB URI
    client = MongoClient(mongo_uri)
    db_name = os.getenv("MONGO_DB_NAME", "my_database")  # Default database name
    db = client[db_name]
    return db
