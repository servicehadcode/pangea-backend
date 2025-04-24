from flask import Blueprint, request, jsonify
from services.discussion_service import DiscussionService
from models.discussion import Discussion
from datetime import datetime

discussion_blueprint = Blueprint('discussion', __name__)
discussion_service = DiscussionService()

@discussion_blueprint.route('/discussions', methods=['POST'])
def create_discussion():
    """
    Create a new discussion or reply.
    
    Request body should contain:
    - problemId: The problem ID
    - content: The discussion content
    - userId: The user ID
    - parentId: (Optional) The parent discussion ID for replies
    
    Returns:
    - JSON response with success message and discussion ID or error
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['problemId', 'content', 'userId']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create discussion object
        discussion = Discussion(
            problem_id=data['problemId'],
            content=data['content'],
            user_id=data['userId'],
            parent_id=data.get('parentId'),
            created_at=datetime.now()
        )
        
        # Save to database
        discussion_id, error = discussion_service.create_discussion(discussion)
        
        if error:
            return jsonify({'error': error}), 500
            
        # Get the created discussion with _id
        created_discussion = discussion_service.get_discussion_by_id(discussion_id)
        
        if not created_discussion:
            return jsonify({'error': 'Failed to retrieve created discussion'}), 500
            
        return jsonify(created_discussion.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@discussion_blueprint.route('/discussions/<problem_id>', methods=['GET'])
def get_discussions(problem_id):
    """
    Get all discussions for a problem.
    
    Args:
        problem_id: The problem ID
        
    Returns:
        JSON response with discussions data or error
    """
    try:
        discussions = discussion_service.get_discussions_by_problem_id(problem_id)
        return jsonify(discussions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@discussion_blueprint.route('/discussions/<discussion_id>/vote', methods=['POST'])
def vote_discussion(discussion_id):
    """
    Add a vote to a discussion.
    
    Args:
        discussion_id: The discussion ID
        
    Returns:
        JSON response with success message or error
    """
    try:
        if discussion_service.add_vote(discussion_id):
            return jsonify({'success': True}), 200
        return jsonify({'error': 'Discussion not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
