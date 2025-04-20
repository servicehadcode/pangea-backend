import json
import requests
import sys

def test_add_problem():
    """
    Test adding a problem with the new schema fields.
    """
    # Sample problem data with new schema fields
    problem_data = {
        "problem_num": "TEST001",
        "title": "Test Problem with New Schema",
        "description": "A test problem to verify the new schema changes",
        "longDescription": "This is a detailed description of the test problem with the new schema fields.",
        "difficulty": "intermediate",
        "category": "test",
        "requirements": {
            "time": "1 week",
            "skills": ["Python", "MongoDB"],
            "prerequisites": ["Basic programming"]
        },
        "tags": ["test", "schema", "update"],
        "steps": [
            {
                "step": 1,
                "description": "First step",
                "details": ["Detail 1", "Detail 2"]
            },
            {
                "step": 2,
                "description": "Second step",
                "details": ["Detail 3", "Detail 4"]
            }
        ],
        "resources": [
            {
                "type": "documentation",
                "url": "https://example.com/docs",
                "description": "Documentation"
            }
        ],
        "metadata": {
            "created": "2024-04-04",
            "author": "Test User",
            "lastUpdated": "2024-04-04",
            "gitRepo": "https://github.com/example/test-repo"
        },
        "acceptanceCriteria": [
            "Criterion 1",
            "Criterion 2"
        ],
        "downloadableItems": [
            "Item 1",
            "Item 2"
        ],
        "preparationSteps": [
            "Preparation step 1",
            "Preparation step 2"
        ]
    }
    
    # API endpoint
    url = "http://localhost:5000/api/addProblem"
    
    # Send the request
    try:
        response = requests.post(url, json=problem_data)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Successfully added problem with new schema")
            return True
        else:
            print("❌ Failed to add problem")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_problem():
    """
    Test retrieving a problem with the new schema fields.
    """
    # API endpoint
    url = "http://localhost:5000/api/problem/TEST001"
    
    # Send the request
    try:
        response = requests.get(url)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            problem = response.json()
            print("Problem retrieved successfully")
            
            # Check if the new fields are present
            new_fields = [
                ('steps[0].details', lambda p: 'details' in p['steps'][0]),
                ('metadata.gitRepo', lambda p: 'gitRepo' in p['metadata']),
                ('acceptanceCriteria', lambda p: 'acceptanceCriteria' in p),
                ('downloadableItems', lambda p: 'downloadableItems' in p),
                ('preparationSteps', lambda p: 'preparationSteps' in p)
            ]
            
            all_fields_present = True
            for field_name, check_func in new_fields:
                if check_func(problem):
                    print(f"✅ Field '{field_name}' is present")
                else:
                    print(f"❌ Field '{field_name}' is missing")
                    all_fields_present = False
            
            # Print the full problem for inspection
            print("\nFull problem data:")
            print(json.dumps(problem, indent=2))
            
            return all_fields_present
        else:
            print(f"❌ Failed to retrieve problem: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_update_problem():
    """
    Test updating a problem with the new schema fields.
    """
    # Updated data
    updated_data = {
        "acceptanceCriteria": [
            "Updated criterion 1",
            "Updated criterion 2",
            "New criterion 3"
        ],
        "steps": [
            {
                "step": 1,
                "description": "Updated first step",
                "details": ["Updated detail 1", "Updated detail 2", "New detail"]
            },
            {
                "step": 2,
                "description": "Updated second step",
                "details": ["Updated detail 3", "Updated detail 4"]
            }
        ],
        "metadata": {
            "gitRepo": "https://github.com/example/updated-repo",
            "lastUpdated": "2024-04-05"
        }
    }
    
    # API endpoint
    url = "http://localhost:5000/api/updateProblem/TEST001"
    
    # Send the request
    try:
        response = requests.put(url, json=updated_data)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Successfully updated problem with new schema fields")
            return True
        else:
            print("❌ Failed to update problem")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_delete_problem():
    """
    Test deleting the test problem.
    """
    # API endpoint
    url = "http://localhost:5000/api/deleteProblem/TEST001"
    
    # Send the request
    try:
        response = requests.delete(url)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Successfully deleted test problem")
            return True
        else:
            print("❌ Failed to delete problem")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """
    Run all tests in sequence.
    """
    print("=" * 50)
    print("TESTING PROBLEM SCHEMA UPDATES")
    print("=" * 50)
    
    # Determine which tests to run
    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        # Only run delete test
        test_delete_problem()
        return
    
    # Run all tests
    print("\n1. Testing adding a problem with new schema...")
    add_success = test_add_problem()
    
    if add_success:
        print("\n2. Testing retrieving a problem with new schema...")
        get_success = test_get_problem()
        
        if get_success:
            print("\n3. Testing updating a problem with new schema...")
            update_success = test_update_problem()
            
            if update_success:
                print("\n4. Testing retrieving the updated problem...")
                get_updated_success = test_get_problem()
                
                print("\n5. Cleaning up - deleting test problem...")
                test_delete_problem()
            else:
                print("\nSkipping remaining tests due to update failure")
        else:
            print("\nSkipping remaining tests due to get failure")
    else:
        print("\nSkipping remaining tests due to add failure")
    
    print("\n" + "=" * 50)
    print("TESTS COMPLETED")
    print("=" * 50)

if __name__ == "__main__":
    main()
