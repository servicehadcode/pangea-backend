from flask import current_app
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timezone

load_dotenv()

class MongoService:
    def __init__(self):
        self.client = None
        self.db = None
        self.user_activity = None
        self.logger = logging.getLogger(__name__)

    def initialize(self):
        """Initialize the MongoDB client and set up collections."""
        try:
            # Try to get MongoDB URI from Flask config first
            mongo_uri = current_app.config.get("MONGO_URI")
            self.logger.info(f"MongoDB URI from config: {mongo_uri}")

            # If not available, fall back to environment variable
            if not mongo_uri:
                mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
                self.logger.warning(f"Using fallback MongoDB URI from environment: {mongo_uri}")

            # Get database name
            db_name = current_app.config.get("MONGO_DB_NAME") or os.getenv("MONGODB_DB", "pangea")
            self.logger.info(f"Using database name: {db_name}")

            # Connect to MongoDB
            self.logger.info(f"Connecting to MongoDB at: {mongo_uri}")
            self.client = MongoClient(mongo_uri)
            self.db = self.client[db_name]

            # Set up collections
            self.logger.info("Setting up user_activity collection")
            self.user_activity = self.db["user_activity"]

            # List all collections to verify
            collection_names = self.db.list_collection_names()
            self.logger.info(f"Available collections: {collection_names}")

            # Check if user_activity exists
            if "user_activity" not in collection_names:
                self.logger.info("Creating user_activity collection")
                self.db.create_collection("user_activity")

            # Verify user_activity is accessible
            self.logger.info(f"Verifying user_activity collection: {self.user_activity is not None}")

            # Insert a test document to verify write access
            test_result = self.user_activity.insert_one({"test": True, "timestamp": datetime.now(timezone.utc)})
            self.logger.info(f"Test document inserted with ID: {test_result.inserted_id}")

            # Delete the test document
            self.user_activity.delete_one({"_id": test_result.inserted_id})
            self.logger.info("Test document deleted")

            self.logger.info(f"MongoDB initialized successfully with database: {db_name}")

            # Test connection
            ping_result = self.db.command('ping')
            self.logger.info(f"MongoDB connection test result: {ping_result}")

        except Exception as e:
            self.logger.error(f"Failed to initialize MongoDB: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            # Don't raise the exception - let the application continue but log the error

    def get_db(self):
        """Get the database instance."""
        if self.db is None:
            self.logger.warning("MongoDB not initialized, attempting to initialize now")
            self.initialize()
            if self.db is None:
                raise RuntimeError("MongoClient not initialized.")
        return self.db

    def ensure_collections(self):
        """Ensure all required collections exist"""
        if self.db is not None:
            collection_names = self.db.list_collection_names()
            if "user_activity" not in collection_names:
                self.db.create_collection("user_activity")
                self.logger.info("Created user_activity collection")
            self.user_activity = self.db["user_activity"]

# Instantiate MongoService
mongo_service = MongoService()
