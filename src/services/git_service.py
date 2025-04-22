from typing import Tuple, Optional, Dict, Any
import os
import json
import requests
from github import Github
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

class GitService:
    def __init__(self):
        # Get GitHub token from environment variable
        self.github_token = os.getenv('GITHUB_TOKEN')
        if not self.github_token:
            # Use the token provided in your original requirements
            self.github_token = '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'
            print(f"Warning: Using hardcoded GitHub token for testing")

        # GitHub username is not strictly needed for API calls with token
        # but we'll use it for consistency with the reference code
        self.github_user = "github-user"  # Default value, not used in API calls

        # Initialize PyGithub client
        self.github = Github(self.github_token)

        # Create a session for direct API calls
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a session for GitHub API requests"""
        # Following the pattern from the reference code
        session = requests.Session()
        # Use basic auth with token as password (same as reference code)
        session.auth = (self.github_user, self.github_token)
        session.headers.update({
            'Accept': 'application/vnd.github.v3+json'
        })
        return session

    def extract_repo_info(self, repo_url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract GitHub username and repo name from a GitHub URL

        Args:
            repo_url: GitHub repository URL

        Returns:
            Tuple of (username, repo_name) or (None, None) if invalid URL
        """
        try:
            # Parse the URL
            parsed_url = urlparse(repo_url)

            # Check if it's a GitHub URL
            if 'github.com' not in parsed_url.netloc:
                return None, None

            # Extract the path and remove leading/trailing slashes
            path = parsed_url.path.strip('/')

            # Split the path into parts
            parts = path.split('/')

            # GitHub repo URLs have the format: github.com/username/repo
            if len(parts) >= 2:
                username = parts[0]
                repo_name = parts[1]
                return username, repo_name

            return None, None
        except Exception:
            return None, None

    def get_full_repo_name(self, repo_url: str) -> Optional[str]:
        """
        Get the full repository name in the format 'username/repo'

        Args:
            repo_url: GitHub repository URL

        Returns:
            Full repository name or None if invalid URL
        """
        username, repo_name = self.extract_repo_info(repo_url)
        if username and repo_name:
            return f"{username}/{repo_name}"
        return None

    def check_branch_exists(self, repo_full_name: str, branch_name: str) -> bool:
        """
        Check if a branch exists in the repository

        Args:
            repo_full_name: Full repository name (username/repo)
            branch_name: Name of the branch to check

        Returns:
            True if branch exists, False otherwise
        """
        try:
            url = f"https://api.github.com/repos/{repo_full_name}/git/ref/heads/{branch_name}"
            print(f"Checking if branch exists: {url}")
            response = self.session.get(url)
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error checking branch: {str(e)}")
            return False

    def get_branch_sha(self, repo_full_name: str, branch_name: str = "main") -> Optional[str]:
        """
        Get the SHA of the latest commit on a branch

        Args:
            repo_full_name: Full repository name (username/repo)
            branch_name: Name of the branch (default: main)

        Returns:
            SHA of the latest commit or None if branch not found
        """
        try:
            # Following the pattern from the reference code
            url = f"https://api.github.com/repos/{repo_full_name}/branches/{branch_name}"
            print(f"Getting SHA for branch '{branch_name}' from URL: {url}")

            response = self.session.get(url)
            print(f"Response status: {response.status_code}")

            if response.status_code > 200:
                print(f"GET error: {response.status_code}")
                print(f"Response body: {response.text}")
                return None

            data = response.json()
            sha = data['commit']['sha']
            print(f"Found SHA: {sha}")
            return sha
        except Exception as e:
            print(f"Error getting branch SHA: {str(e)}")
            return None

    def create_branch(self, repo_full_name: str, new_branch_name: str, base_branch_name: str = "main") -> Tuple[bool, Dict[str, Any]]:
        """
        Create a new branch in the repository

        Args:
            repo_full_name: Full repository name (username/repo)
            new_branch_name: Name of the new branch to create
            base_branch_name: Name of the branch to base the new branch on (default: main)

        Returns:
            Tuple of (success, response_data)
        """
        try:
            print(f"Creating branch '{new_branch_name}' in repo '{repo_full_name}' based on '{base_branch_name}'")

            # Get the SHA of the base branch
            base_sha = self.get_branch_sha(repo_full_name, base_branch_name)
            print(f"Base branch SHA: {base_sha}")

            if not base_sha:
                print(f"Base branch '{base_branch_name}' not found")
                return False, {"error": f"Base branch '{base_branch_name}' not found"}

            # Create the new branch - following the pattern from the reference code
            url = f"https://api.github.com/repos/{repo_full_name}/git/refs"
            data = json.dumps({
                "ref": f"refs/heads/{new_branch_name}",
                "sha": base_sha
            })

            print(f"Creating branch with URL: {url}")
            print(f"Payload: {data}")

            # Use the session directly like in the reference code
            response = self.session.post(url, data=data)

            print(f"Response status: {response.status_code}")

            if response.status_code not in [200, 201]:
                print(f"POST error: {response.status_code}, {response.text}")
                return False, {"error": f"Failed to create branch: {response.text}"}

            print(f"✅ Branch '{new_branch_name}' created successfully.")
            return True, response.json()
        except Exception as e:
            print(f"Error creating branch: {str(e)}")
            return False, {"error": str(e)}

    def create_pull_request(self, repo_full_name: str, head: str, base: str, title: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Create a new pull request in the repository

        Args:
            repo_full_name: Full repository name (username/repo)
            head: The name of the branch where your changes are implemented
            base: The name of the branch you want the changes pulled into
            title: The title of the pull request

        Returns:
            Tuple of (success, response_data)
        """
        try:
            print(f"Creating PR from '{head}' into '{base}' in repo '{repo_full_name}'")

            # Create the pull request
            url = f"https://api.github.com/repos/{repo_full_name}/pulls"
            data = json.dumps({
                "title": title,
                "head": head,
                "base": base,
                "body": f"Pull request created via API: {title}"
            })

            print(f"Creating PR with URL: {url}")
            print(f"Payload: {data}")

            response = self.session.post(url, data=data)

            print(f"Response status: {response.status_code}")

            if response.status_code not in [200, 201]:
                print(f"POST error: {response.status_code}, {response.text}")
                return False, {"error": f"Failed to create PR: {response.text}"}

            print(f"✅ Pull request '{title}' created successfully.")
            return True, response.json()
        except Exception as e:
            print(f"Error creating PR: {str(e)}")
            return False, {"error": str(e)}

    def get_pull_request_diff(self, repo_full_name: str, pr_number: int) -> Tuple[bool, str]:
        """
        Get the diff for a pull request

        Args:
            repo_full_name: Full repository name (username/repo)
            pr_number: The pull request number

        Returns:
            Tuple of (success, diff_content)
        """
        try:
            print(f"Getting diff for PR #{pr_number} in repo '{repo_full_name}'")

            # Get the diff
            url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"
            headers = self.session.headers.copy()
            headers.update({"Accept": "application/vnd.github.v3.diff"})

            print(f"Getting diff with URL: {url}")

            response = requests.get(url, headers=headers, auth=self.session.auth)

            print(f"Response status: {response.status_code}")

            if response.status_code != 200:
                print(f"GET error: {response.status_code}, {response.text}")
                return False, f"Failed to get PR diff: {response.text}"

            print(f"✅ Pull request diff retrieved successfully.")
            return True, response.text
        except Exception as e:
            print(f"Error getting PR diff: {str(e)}")
            return False, str(e)
