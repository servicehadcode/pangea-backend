import requests
import json
import sys
import pymongo
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
client = pymongo.MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'))
db = client[os.getenv('MONGODB_DB', 'pangea')]

# API base URL
BASE_URL = "http://localhost:5000/api"

def check_server_running():
    """Check if the Flask server is running."""
    try:
        response = requests.get(f"{BASE_URL}/problems", timeout=2)
        return response.status_code == 200
    except:
        return False

def setup_test_data():
    """
    Set up test data in the database.

    Returns:
        Tuple of (problem_id, discussion_id)
    """
    # Clear existing test discussions
    db.discussions.delete_many({"problemId": "TEST001"})

    # Create a test discussion
    discussion = {
        "problemId": "TEST001",
        "content": "This is a test discussion",
        "userId": "test-user-123",
        "parentId": None,
        "votes": 0,
        "createdAt": datetime.now().isoformat()
    }

    # Insert the discussion
    result = db.discussions.insert_one(discussion)
    discussion_id = str(result.inserted_id)

    print(f"Created test discussion with ID: {discussion_id}")
    return "TEST001", discussion_id

def test_create_discussion():
    """Test creating a new discussion."""
    url = f"{BASE_URL}/discussions"
    
    payload = {
        "problemId": "TEST001",
        "content": "This is a new test discussion",
        "userId": "test-user-456"
    }
    
    print(f"\nTesting create discussion endpoint with payload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"Response:\n{json.dumps(data, indent=2)}")
            print("\n✅ SUCCESS: Create discussion API works!")
            return True
        else:
            print(f"Response:\n{json.dumps(response.json(), indent=2)}")
            print("\n❌ FAILURE: Create discussion API failed")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_get_discussions(problem_id):
    """Test getting discussions for a problem."""
    url = f"{BASE_URL}/discussions/{problem_id}"
    
    print(f"\nTesting get discussions endpoint for problem ID: {problem_id}")
    
    try:
        response = requests.get(url)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response:\n{json.dumps(data, indent=2)}")
            print("\n✅ SUCCESS: Get discussions API works!")
            return True
        else:
            print(f"Response:\n{json.dumps(response.json(), indent=2)}")
            print("\n❌ FAILURE: Get discussions API failed")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_create_reply(discussion_id):
    """Test creating a reply to a discussion."""
    url = f"{BASE_URL}/discussions"
    
    payload = {
        "problemId": "TEST001",
        "content": "This is a reply to the test discussion",
        "userId": "test-user-789",
        "parentId": discussion_id
    }
    
    print(f"\nTesting create reply endpoint with payload:\n{json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"Response:\n{json.dumps(data, indent=2)}")
            print("\n✅ SUCCESS: Create reply API works!")
            return True
        else:
            print(f"Response:\n{json.dumps(response.json(), indent=2)}")
            print("\n❌ FAILURE: Create reply API failed")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_vote_discussion(discussion_id):
    """Test voting on a discussion."""
    url = f"{BASE_URL}/discussions/{discussion_id}/vote"
    
    print(f"\nTesting vote discussion endpoint for discussion ID: {discussion_id}")
    
    try:
        response = requests.post(url)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response:\n{json.dumps(data, indent=2)}")
            print("\n✅ SUCCESS: Vote discussion API works!")
            return True
        else:
            print(f"Response:\n{json.dumps(response.json(), indent=2)}")
            print("\n❌ FAILURE: Vote discussion API failed")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    """
    Main function to run all tests.
    """
    # Check if server is running
    if not check_server_running():
        print("\n❌ Error: Flask server is not running. Please start the server with 'python src/app.py' and try again.")
        return

    try:
        # Set up test data
        problem_id, discussion_id = setup_test_data()
        
        # Run tests
        test_create_discussion()
        test_get_discussions(problem_id)
        test_create_reply(discussion_id)
        test_vote_discussion(discussion_id)
        
        print("\n✅ All tests completed!")
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("Testing Discussions API")
    print("=" * 50)
    main()
