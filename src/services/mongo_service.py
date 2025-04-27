from flask import current_app
from pymongo import MongoClient

class MongoService:
    def __init__(self):
        self.client = None
        self.db = None
        self.user_activity = None

    def initialize(self):
        """Initialize the MongoDB client and set up collections."""
        self.client = MongoClient(current_app.config["MONGO_URI"])
        self.db = self.client.get_database()  # Get the database
        self.user_activity = self.db["user_activity"]  # Define the collection

    def get_db(self):
        """Get the database instance."""
        if self.db is None:
            raise RuntimeError("MongoClient not initialized.")
        return self.db

# Instantiate MongoService
mongo_service = MongoService()
