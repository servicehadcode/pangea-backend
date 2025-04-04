from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')

# This will create the database if it doesn't exist
db = client.pangea

# This will create the collection if it doesn't exist
problems = db.problems

# Insert a test document
test_problem = {
    "problem_num": "TEST001",
    "title": "Test Problem",
    "description": "Test Description",
    "longDescription": "Long Test Description",
    "difficulty": "easy",
    "category": "test",
    "requirements": {},
    "tags": ["test"],
    "steps": [],
    "resources": [],
    "metadata": {}
}

# Insert the document
result = problems.insert_one(test_problem)
print(f"Inserted document ID: {result.inserted_id}")

# Verify it exists
found = problems.find_one({"problem_num": "TEST001"})
print("Found document:", found)

# Clean up
problems.delete_one({"problem_num": "TEST001"})