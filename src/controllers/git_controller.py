from flask import Blueprint, request, jsonify
from services.git_service import GitService

git_blueprint = Blueprint('git', __name__)
git_service = GitService()

@git_blueprint.route('/git/create-branch', methods=['POST'])
def create_branch():
    """
    Create a new branch in a GitHub repository

    Request body should contain:
    - repoUrl: The GitHub repository URL
    - username: The GitHub username to use in the branch name
    - branchOff: (Optional) The branch to base the new branch on (default: main)
    - branchTo: (Optional) The name of the new branch (default: {username}-{branchOff})

    Returns:
        JSON response with success message or error
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['repoUrl', 'username']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        repo_url = data['repoUrl']
        username = data['username']
        branch_off = data.get('branchOff', 'main')

        # Get the full repo name (username/repo)
        repo_full_name = git_service.get_full_repo_name(repo_url)
        if not repo_full_name:
            return jsonify({'error': 'Invalid GitHub repository URL'}), 400

        # Create the branch name in the format username-main or use provided branchTo
        new_branch_name = data.get('branchTo', f"{username}-{branch_off}")

        # Check if branch already exists
        if git_service.check_branch_exists(repo_full_name, new_branch_name):
            # Branch already exists, return success with a message
            return jsonify({
                'message': f"Branch '{new_branch_name}' already exists",
                'branchName': new_branch_name,
                'alreadyExists': True,
                'gitCommands': [
                    f"git clone -b {new_branch_name} --single-branch https://github.com/{repo_full_name}"
                ]
            }), 200

        # Create the branch
        success, response = git_service.create_branch(repo_full_name, new_branch_name, branch_off)

        if success:
            return jsonify({
                'message': f"Branch '{new_branch_name}' created successfully",
                'branchName': new_branch_name,
                'alreadyExists': False,
                'gitCommands': [
                    f"git clone -b {new_branch_name} --single-branch https://github.com/{repo_full_name}"
                ]
            }), 201
        else:
            return jsonify({'error': response.get('error', 'Failed to create branch')}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@git_blueprint.route('/git/create-pr', methods=['POST'])
def create_pull_request():
    """
    Create a new pull request

    Request body should contain:
    - repoUrl: The GitHub repository URL
    - head: The name of the branch where your changes are implemented
    - base: The name of the branch you want the changes pulled into
    - title: The title of the pull request

    Returns:
        JSON response with PR details or error
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['repoUrl', 'head', 'base', 'title']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        repo_url = data['repoUrl']
        head = data['head']
        base = data['base']
        title = data['title']

        # Get the full repo name (username/repo)
        repo_full_name = git_service.get_full_repo_name(repo_url)
        if not repo_full_name:
            return jsonify({'error': 'Invalid GitHub repository URL'}), 400

        # Create the pull request
        success, response = git_service.create_pull_request(repo_full_name, head, base, title)

        if not success:
            return jsonify({'error': response.get('error', 'Failed to create pull request')}), 400

        # Get the PR number from the response
        pr_number = response.get('number')
        if not pr_number:
            return jsonify({'error': 'Failed to get pull request number'}), 500

        # Get the PR diff
        diff_success, diff_content = git_service.get_pull_request_diff(repo_full_name, pr_number)

        if not diff_success:
            return jsonify({
                'pr_title': title,
                'pr_number': pr_number,
                'error': f'Pull request created but failed to get diff: {diff_content}'
            }), 201

        # Return the PR details
        return jsonify({
            'pr_title': title,
            'pr_number': pr_number,
            'pr_diff': diff_content
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
