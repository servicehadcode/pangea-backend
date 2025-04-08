import requests
import json
from datetime import datetime
# No need to import ObjectId as we're using string IDs
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
client = pymongo.MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'))
db = client[os.getenv('MONGODB_DB', 'pangea')]

# API base URL
BASE_URL = "http://localhost:5000/api"

def setup_test_data():
    """
    Set up test data in the database.

    Returns:
        Tuple of (problem_instance_id, subtask_instance_id)
    """
    # Clear existing test data
    db.problem_instances.delete_many({"problemNum": "TEST001"})
    db.subtask_instances.delete_many({})

    # Create a test problem instance
    problem_instance = {
        "problemNum": "TEST001",
        "owner": {
            "userId": "test-user-123",
            "username": "testuser",
            "email": "test@example.com"
        },
        "collaborationMode": "solo",
        "collaborators": [
            {
                "userId": "collab-user-456",
                "username": "collaborator",
                "email": "collab@example.com",
                "invitedAt": datetime.now().isoformat(),
                "joinedAt": datetime.now().isoformat(),
                "status": "active"
            }
        ],
        "status": "in-progress",
        "startedAt": datetime.now().isoformat(),
        "lastUpdatedAt": datetime.now().isoformat(),
        "completedAt": None
    }

    # Insert the problem instance
    result = db.problem_instances.insert_one(problem_instance)
    problem_instance_id = str(result.inserted_id)

    # Create a test subtask instance
    subtask_instance = {
        "problemInstanceId": problem_instance_id,
        "stepNum": 1,
        "assignee": {
            "userId": "test-user-123",
            "username": "testuser"
        },
        "reporter": {
            "userId": "collab-user-456",
            "username": "collaborator"
        },
        "status": "in-progress",
        "branchCreated": True,
        "prCreated": False,
        "deliverables": "Test deliverables",
        "acceptanceCriteria": [
            {
                "criteriaText": "Test criterion 1",
                "completed": True
            },
            {
                "criteriaText": "Test criterion 2",
                "completed": False
            }
        ],
        "prFeedback": [],
        "startedAt": datetime.now().isoformat(),
        "completedAt": None
    }

    # Insert the subtask instance
    result = db.subtask_instances.insert_one(subtask_instance)
    subtask_instance_id = str(result.inserted_id)

    return problem_instance_id, subtask_instance_id

def test_get_problem_instance():
    """
    Test the GET /api/problem-instances/:problemNum/:userId endpoint.
    """
    print("\n=== Testing GET Problem Instance ===")

    # Make the request
    url = f"{BASE_URL}/problem-instances/TEST001/test-user-123"
    print(f"Sending GET request to: {url}")

    response = requests.get(url)

    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Verify the response
    assert response.status_code == 200, "Expected status code 200"
    assert response.json()["problemNum"] == "TEST001", "Expected problem number TEST001"
    assert response.json()["owner"]["userId"] == "test-user-123", "Expected owner userId test-user-123"

    return response.json()

def test_get_subtask_instances(problem_instance_id):
    """
    Test the GET /api/problem-instances/:instanceId/subtasks endpoint.
    """
    print("\n=== Testing GET Subtask Instances ===")

    # Make the request
    url = f"{BASE_URL}/problem-instances/{problem_instance_id}/subtasks"
    print(f"Sending GET request to: {url}")

    response = requests.get(url)

    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Verify the response
    assert response.status_code == 200, "Expected status code 200"
    assert len(response.json()) > 0, "Expected at least one subtask instance"
    assert response.json()[0]["problemInstanceId"] == problem_instance_id, f"Expected problemInstanceId {problem_instance_id}"

    return response.json()

def test_get_collaborators(problem_instance_id):
    """
    Test the GET /api/problem-instances/:instanceId/collaborators endpoint.
    """
    print("\n=== Testing GET Collaborators ===")

    # Make the request
    url = f"{BASE_URL}/problem-instances/{problem_instance_id}/collaborators"
    print(f"Sending GET request to: {url}")

    response = requests.get(url)

    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Verify the response
    assert response.status_code == 200, "Expected status code 200"
    assert len(response.json()) > 0, "Expected at least one collaborator"
    assert response.json()[0]["userId"] == "collab-user-456", "Expected userId collab-user-456"

    return response.json()

def test_get_subtask_instance(subtask_instance_id):
    """
    Test the GET /api/subtask-instances/:subtaskId endpoint.
    """
    print("\n=== Testing GET Subtask Instance ===")

    # Make the request
    url = f"{BASE_URL}/subtask-instances/{subtask_instance_id}"
    print(f"Sending GET request to: {url}")

    response = requests.get(url)

    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Verify the response
    assert response.status_code == 200, "Expected status code 200"
    assert response.json()["_id"] == subtask_instance_id, f"Expected _id {subtask_instance_id}"

    return response.json()

def check_server_running():
    """
    Check if the Flask server is running.
    """
    try:
        requests.get(f"{BASE_URL}/problems")
        return True
    except requests.exceptions.ConnectionError:
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
        problem_instance_id, subtask_instance_id = setup_test_data()
        print(f"Created test problem instance with ID: {problem_instance_id}")
        print(f"Created test subtask instance with ID: {subtask_instance_id}")

        # Run tests
        test_get_problem_instance()
        test_get_subtask_instances(problem_instance_id)
        test_get_collaborators(problem_instance_id)
        test_get_subtask_instance(subtask_instance_id)

        print("\n✅ All tests passed!")

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
    finally:
        # Clean up test data
        db.problem_instances.delete_many({"problemNum": "TEST001"})
        db.subtask_instances.delete_many({"problemInstanceId": problem_instance_id})
        print("\nTest data cleaned up.")

if __name__ == "__main__":
    main()
