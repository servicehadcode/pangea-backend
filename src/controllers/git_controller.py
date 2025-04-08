from flask import Blueprint, request, jsonify
from services.git_service import GitService

git_blueprint = Blueprint('git', __name__)
git_service = GitService()

@git_blueprint.route('/startDevelopment', methods=['POST'])
def start_development():
    """
    Endpoint to start development by creating a new remote branch.
    
    Expects:
    - gitRepo: URL of the Git repository
    - branchNm: Name of the branch to create
    
    Returns:
    - JSON response with success status, message, and commands to execute
    """
    try:
        # Get request data
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'MISSING_DATA',
                    'message': 'No data provided',
                    'details': None
                }
            }), 400
            
        git_repo = data.get('gitRepo')
        branch_name = data.get('branchNm')
        
        if not git_repo:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'MISSING_REPO',
                    'message': 'Git repository URL is required',
                    'details': None
                }
            }), 400
            
        if not branch_name:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'MISSING_BRANCH',
                    'message': 'Branch name is required',
                    'details': None
                }
            }), 400
        
        # Create the remote branch
        success, result = git_service.create_remote_branch(git_repo, branch_name)
        
        if success:
            return jsonify({
                'success': True,
                'data': result
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'BRANCH_CREATION_FAILED',
                    'message': 'Failed to create remote branch',
                    'details': result
                }
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'SERVER_ERROR',
                'message': 'An unexpected error occurred',
                'details': str(e)
            }
        }), 500
