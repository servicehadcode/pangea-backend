from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client.pangea

# Get the user_activity collection
user_activity = db.user_activity

# Count documents before deletion
count_before = user_activity.count_documents({})
print(f"Documents in user_activity before deletion: {count_before}")

# Delete all documents
result = user_activity.delete_many({})
print(f"Deleted {result.deleted_count} documents from user_activity collection")

# Verify collection is empty
count_after = user_activity.count_documents({})
print(f"Documents in user_activity after deletion: {count_after}")

# Close the connection
client.close()
