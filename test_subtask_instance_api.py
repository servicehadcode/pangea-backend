import requests
import json
from datetime import datetime
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
    db.problem_instances.delete_many({"problemNum": "TEST002"})
    db.subtask_instances.delete_many({"problemInstanceId": {"$regex": "test"}})

    # Create a test problem instance
    problem_instance = {
        "problemNum": "TEST002",
        "owner": {
            "userId": "test-user-789",
            "username": "testuser2",
            "email": "test2@example.com"
        },
        "collaborationMode": "pair",
        "collaborators": [
            {
                "userId": "collab-user-101",
                "username": "collaborator2",
                "email": "collab2@example.com",
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

    # Create test subtask instances
    subtask_instances = [
        {
            "problemInstanceId": problem_instance_id,
            "stepNum": 1,
            "assignee": {
                "userId": "test-user-789",
                "username": "testuser2"
            },
            "reporter": {
                "userId": "collab-user-101",
                "username": "collaborator2"
            },
            "status": "in-progress",
            "branchCreated": True,
            "prCreated": False,
            "deliverables": "First step deliverables",
            "acceptanceCriteria": [
                {
                    "criteriaText": "First step criterion 1",
                    "completed": True
                },
                {
                    "criteriaText": "First step criterion 2",
                    "completed": False
                }
            ],
            "prFeedback": [],
            "startedAt": datetime.now().isoformat(),
            "completedAt": None
        },
        {
            "problemInstanceId": problem_instance_id,
            "stepNum": 2,
            "assignee": {
                "userId": "collab-user-101",
                "username": "collaborator2"
            },
            "reporter": {
                "userId": "test-user-789",
                "username": "testuser2"
            },
            "status": "not-started",
            "branchCreated": False,
            "prCreated": False,
            "deliverables": "",
            "acceptanceCriteria": [
                {
                    "criteriaText": "Second step criterion 1",
                    "completed": False
                },
                {
                    "criteriaText": "Second step criterion 2",
                    "completed": False
                }
            ],
            "prFeedback": [],
            "startedAt": None,
            "completedAt": None
        }
    ]

    # Insert the subtask instances
    result = db.subtask_instances.insert_many(subtask_instances)
    subtask_instance_ids = [str(id) for id in result.inserted_ids]

    return problem_instance_id, subtask_instance_ids

def test_get_subtask_instance(subtask_id):
    """
    Test the GET /api/subtask-instances/:subtaskId endpoint.
    """
    print(f"\n=== Testing GET Subtask Instance (ID: {subtask_id}) ===")

    # Make the request
    url = f"{BASE_URL}/subtask-instances/{subtask_id}"
    print(f"Sending GET request to: {url}")

    response = requests.get(url)

    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Verify the response
    assert response.status_code == 200, "Expected status code 200"
    assert response.json()["_id"] == subtask_id, f"Expected _id {subtask_id}"

    return response.json()

def test_get_subtasks_for_problem_instance(problem_instance_id):
    """
    Test the GET /api/problem-instances/:instanceId/subtasks endpoint.
    """
    print(f"\n=== Testing GET Subtasks for Problem Instance (ID: {problem_instance_id}) ===")

    # Make the request
    url = f"{BASE_URL}/problem-instances/{problem_instance_id}/subtasks"
    print(f"Sending GET request to: {url}")

    response = requests.get(url)

    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Verify the response
    assert response.status_code == 200, "Expected status code 200"
    assert len(response.json()) == 2, "Expected 2 subtask instances"

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
        problem_instance_id, subtask_instance_ids = setup_test_data()
        print(f"Created test problem instance with ID: {problem_instance_id}")
        print(f"Created test subtask instances with IDs: {', '.join(subtask_instance_ids)}")

        # Run tests
        for subtask_id in subtask_instance_ids:
            test_get_subtask_instance(subtask_id)

        test_get_subtasks_for_problem_instance(problem_instance_id)

        print("\n✅ All tests passed!")

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
    finally:
        # Clean up test data
        db.problem_instances.delete_many({"problemNum": "TEST002"})
        db.subtask_instances.delete_many({"problemInstanceId": problem_instance_id})
        print("\nTest data cleaned up.")

if __name__ == "__main__":
    main()
