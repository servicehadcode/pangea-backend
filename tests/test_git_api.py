import requests
import json
import time

def test_start_development():
    """
    Test the startDevelopment API endpoint.
    """
    # API endpoint
    url = "http://localhost:5000/api/startDevelopment"

    # Test data - replace with your actual repository URL and branch name
    data = {
        "gitRepo": "https://github.com/servicehadcode/pangea-gitFlow-test.git",
        "branchNm": f"feature/test-branch-{int(time.time())}"
    }

    # Make the request
    print(f"Sending request to {url} with data: {json.dumps(data, indent=2)}")
    response = requests.post(url, json=data)

    # Print the response
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Check if the request was successful
    if response.status_code == 201:
        print("✅ API call successful")

        # Check if the response has the expected structure
        response_data = response.json()
        if response_data.get('success') and 'data' in response_data:
            print("✅ Response has the expected structure")

            # Check if the data contains the message and commands
            data = response_data.get('data')
            if 'message' in data and 'commands' in data:
                print("✅ Response contains message and commands")

                # Print the commands
                print("\nCommands to execute:")
                for i, command in enumerate(data['commands']):
                    print(f"{i+1}. {command}")
            else:
                print("❌ Response is missing message or commands")
        else:
            print("❌ Response does not have the expected structure")
    else:
        print("❌ API call failed")

if __name__ == "__main__":
    test_start_development()
