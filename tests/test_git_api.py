import requests
import json
import sys

# Try both ports 5000 and 5001
def get_base_url():
    # Try port 5000 first
    try:
        response = requests.get("http://localhost:5000")
        return "http://localhost:5000/api"
    except requests.exceptions.ConnectionError:
        # Try port 5001
        try:
            response = requests.get("http://localhost:5001")
            return "http://localhost:5001/api"
        except requests.exceptions.ConnectionError:
            # Default to 5000 if neither is available
            return "http://localhost:5000/api"

BASE_URL = get_base_url()

def test_create_branch():
    """Test the create-branch endpoint"""
    url = f"{BASE_URL}/git/create-branch"

    # Use a valid GitHub repository URL
    repo_url = "https://github.com/servicehadcode/pangea-gitFlow-test"

    # Generate a unique branch name for testing
    import random
    new_branch_name = f"test-branch-{random.randint(1000, 9999)}"

    payload = {
        "repoUrl": repo_url,
        "username": "testuser",
        "branchOff": "main",
        "branchTo": new_branch_name  # Use the generated branch name
    }

    print(f"Testing create-branch endpoint with payload:\n{json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=10)

        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")

        if response.status_code in [200, 201]:
            print("\n✅ SUCCESS: Branch creation API works!")

            # Print the Git commands for the user
            data = response.json()
            if 'gitCommands' in data:
                print("\nGit commands to use the branch:")
                for cmd in data['gitCommands']:
                    print(f"  $ {cmd}")

            return True
        else:
            print("\n❌ FAILURE: Branch creation API failed")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Git API - Create Branch")
    print("=" * 50)

    if test_create_branch():
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")
        sys.exit(1)