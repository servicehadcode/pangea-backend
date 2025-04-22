import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def test_create_pull_request():
    """Test the git/create-pr endpoint"""
    url = f"{BASE_URL}/git/create-pr"

    # Use a valid GitHub repository URL
    repo_url = "https://github.com/servicehadcode/pangea-gitFlow-test"

    payload = {
        "repoUrl": repo_url,
        "head": "had-feature",
        "base": "had-main",
        "title": "Test PR created via API"
    }

    print(f"Testing create-pull-request endpoint with payload:\n{json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=30)  # Longer timeout for PR creation

        print(f"Status Code: {response.status_code}")

        if response.status_code in [200, 201]:
            data = response.json()
            print(f"Response:\n{json.dumps({k: v for k, v in data.items() if k != 'pr_diff'}, indent=2)}")
            print(f"\nDiff preview (first 300 chars):\n{data.get('pr_diff', '')[:300]}...")
            print("\n✅ SUCCESS: Pull request creation API works!")
            return True
        else:
            print(f"Response:\n{json.dumps(response.json(), indent=2)}")
            print("\n❌ FAILURE: Pull request creation API failed")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing PR API - Create Pull Request")
    print("=" * 50)

    if test_create_pull_request():
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")
        sys.exit(1)
