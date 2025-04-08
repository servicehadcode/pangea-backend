import requests
import json
import pymongo
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# MongoDB connection
client = pymongo.MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'))
db = client[os.getenv('MONGODB_DB', 'pangea')]

# API base URL
BASE_URL = "http://localhost:5000/api"

def clean_test_data():
    """
    Clean up any existing test data.
    """
    db.problem_instances.delete_many({"problemNum": "TEST003"})
    db.subtask_instances.delete_many({"problemInstanceId": {"$regex": "test"}})

def test_create_problem_instance():
    """
    Test the POST /api/problem-instances endpoint.
    """
    print("\n=== Testing POST Create Problem Instance ===")
    
    # Prepare the request data
    data = {
        "problemNum": "TEST003",
        "owner": {
            "userId": "test-user-999",
            "username": "testuser3",
            "email": "test3@example.com"
        },
        "collaborationMode": "pair"
    }
    
    # Make the request
    url = f"{BASE_URL}/problem-instances"
    print(f"Sending POST request to: {url}")
    print(f"Request data: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    
    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Verify the response
    assert response.status_code == 201, "Expected status code 201"
    assert "instanceId" in response.json(), "Expected instanceId in response"
    
    return response.json()["instanceId"]

def test_add_collaborator(instance_id):
    """
    Test the POST /api/problem-instances/:instanceId/collaborators endpoint.
    """
    print("\n=== Testing POST Add Collaborator ===")
    
    # Prepare the request data
    data = {
        "userId": "collab-user-888",
        "username": "collaborator3",
        "email": "collab3@example.com"
    }
    
    # Make the request
    url = f"{BASE_URL}/problem-instances/{instance_id}/collaborators"
    print(f"Sending POST request to: {url}")
    print(f"Request data: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    
    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Verify the response
    assert response.status_code == 200, "Expected status code 200"
    assert "message" in response.json(), "Expected message in response"
    
    return response.json()

def test_create_subtask_instance(instance_id):
    """
    Test the POST /api/problem-instances/:instanceId/subtasks endpoint.
    """
    print("\n=== Testing POST Create Subtask Instance ===")
    
    # Prepare the request data
    data = {
        "stepNum": 1,
        "assignee": {
            "userId": "test-user-999",
            "username": "testuser3"
        },
        "reporter": {
            "userId": "collab-user-888",
            "username": "collaborator3"
        },
        "status": "not-started",
        "acceptanceCriteria": [
            {
                "criteriaText": "Test criterion 1",
                "completed": False
            },
            {
                "criteriaText": "Test criterion 2",
                "completed": False
            }
        ]
    }
    
    # Make the request
    url = f"{BASE_URL}/problem-instances/{instance_id}/subtasks"
    print(f"Sending POST request to: {url}")
    print(f"Request data: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    
    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Verify the response
    assert response.status_code == 201, "Expected status code 201"
    assert "subtaskId" in response.json(), "Expected subtaskId in response"
    
    return response.json()["subtaskId"]

def test_update_problem_instance_status(instance_id):
    """
    Test the PATCH /api/problem-instances/:instanceId endpoint.
    """
    print("\n=== Testing PATCH Update Problem Instance Status ===")
    
    # Prepare the request data
    data = {
        "status": "completed"
    }
    
    # Make the request
    url = f"{BASE_URL}/problem-instances/{instance_id}"
    print(f"Sending PATCH request to: {url}")
    print(f"Request data: {json.dumps(data, indent=2)}")
    
    response = requests.patch(url, json=data)
    
    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Verify the response
    assert response.status_code == 200, "Expected status code 200"
    assert "message" in response.json(), "Expected message in response"
    
    return response.json()

def test_update_subtask_instance(instance_id, subtask_id):
    """
    Test the PATCH /api/problem-instances/:instanceId/subtasks/:subtaskId endpoint.
    """
    print("\n=== Testing PATCH Update Subtask Instance ===")
    
    # Prepare the request data
    data = {
        "status": "in-progress",
        "branchCreated": True,
        "deliverables": "Test deliverables for the subtask"
    }
    
    # Make the request
    url = f"{BASE_URL}/problem-instances/{instance_id}/subtasks/{subtask_id}"
    print(f"Sending PATCH request to: {url}")
    print(f"Request data: {json.dumps(data, indent=2)}")
    
    response = requests.patch(url, json=data)
    
    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Verify the response
    assert response.status_code == 200, "Expected status code 200"
    assert "message" in response.json(), "Expected message in response"
    
    return response.json()

def test_update_acceptance_criteria(instance_id, subtask_id):
    """
    Test the PATCH /api/problem-instances/:instanceId/subtasks/:subtaskId/criteria/:criteriaId endpoint.
    """
    print("\n=== Testing PATCH Update Acceptance Criteria ===")
    
    # Prepare the request data
    data = {
        "completed": True
    }
    
    # Make the request for the first criterion (index 0)
    criteria_id = "0"
    url = f"{BASE_URL}/problem-instances/{instance_id}/subtasks/{subtask_id}/criteria/{criteria_id}"
    print(f"Sending PATCH request to: {url}")
    print(f"Request data: {json.dumps(data, indent=2)}")
    
    response = requests.patch(url, json=data)
    
    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Verify the response
    assert response.status_code == 200, "Expected status code 200"
    assert "message" in response.json(), "Expected message in response"
    
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
        # Clean up any existing test data
        clean_test_data()
        
        # Run tests
        instance_id = test_create_problem_instance()
        test_add_collaborator(instance_id)
        subtask_id = test_create_subtask_instance(instance_id)
        
        # Wait a bit to ensure data is saved
        time.sleep(1)
        
        test_update_subtask_instance(instance_id, subtask_id)
        test_update_acceptance_criteria(instance_id, subtask_id)
        test_update_problem_instance_status(instance_id)
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
    finally:
        # Clean up test data
        clean_test_data()
        print("\nTest data cleaned up.")

if __name__ == "__main__":
    main()
