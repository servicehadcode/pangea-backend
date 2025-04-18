from flask import Blueprint, request, jsonify
from services.problem_instance_service import ProblemInstanceService
from services.subtask_instance_service import SubtaskInstanceService
from models.problem_instance import ProblemInstance
from models.subtask_instance import SubtaskInstance

problem_instance_blueprint = Blueprint('problem_instance', __name__)
problem_instance_service = ProblemInstanceService()
subtask_instance_service = SubtaskInstanceService()

@problem_instance_blueprint.route('/problem-instances/<problem_num>/<user_id>', methods=['GET'])
def get_problem_instance(problem_num, user_id):
    """
    Get a specific problem instance for a user and problem.

    Args:
        problem_num: The problem number
        user_id: The user ID

    Returns:
        JSON response with problem instance data or error
    """
    try:
        instance = problem_instance_service.get_problem_instance(problem_num, user_id)
        if not instance:
            return jsonify({'error': 'Problem instance not found'}), 404
        return jsonify(instance.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@problem_instance_blueprint.route('/problem-instances/<instance_id>/subtasks', methods=['GET'])
def get_subtask_instances(instance_id):
    """
    Get all subtask instances for a problem instance.

    Args:
        instance_id: The problem instance ID

    Returns:
        JSON response with subtask instances data or error
    """
    try:
        # First check if the problem instance exists
        instance = problem_instance_service.get_problem_instance_by_id(instance_id)
        if not instance:
            return jsonify({'error': 'Problem instance not found'}), 404

        subtasks = subtask_instance_service.get_subtask_instances(instance_id)
        return jsonify([subtask.to_dict() for subtask in subtasks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@problem_instance_blueprint.route('/problem-instances/<instance_id>/collaborators', methods=['GET'])
def get_collaborators(instance_id):
    """
    Get all collaborators for a problem instance.

    Args:
        instance_id: The problem instance ID

    Returns:
        JSON response with collaborators data or error
    """
    try:
        # First check if the problem instance exists
        instance = problem_instance_service.get_problem_instance_by_id(instance_id)
        if not instance:
            return jsonify({'error': 'Problem instance not found'}), 404

        collaborators = problem_instance_service.get_collaborators(instance_id)
        return jsonify(collaborators), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@problem_instance_blueprint.route('/problem-instances', methods=['POST'])
def create_problem_instance():
    """
    Create a new problem instance.

    Request body should contain:
    - problemNum: The problem number
    - owner: Object with userId, username, and email
    - collaborationMode: 'solo' or 'pair'

    Returns:
        JSON response with success message and instance ID, or error
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get('problemNum'):
            return jsonify({'error': 'Problem number is required'}), 400

        if not data.get('owner') or not data.get('owner').get('userId'):
            return jsonify({'error': 'Owner information is required'}), 400

        if not data.get('collaborationMode'):
            return jsonify({'error': 'Collaboration mode is required'}), 400

        # Create the problem instance
        instance_id, error = problem_instance_service.create_problem_instance(data)

        if error:
            return jsonify({'error': error}), 400

        return jsonify({
            'message': 'Problem instance created successfully',
            'instanceId': instance_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@problem_instance_blueprint.route('/problem-instances/<instance_id>/collaborators', methods=['POST'])
def add_collaborator(instance_id):
    """
    Add a collaborator to a problem instance.

    Request body should contain:
    - userId: The user ID of the collaborator
    - username: The username of the collaborator
    - email: The email of the collaborator

    Returns:
        JSON response with success message or error
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get('userId'):
            return jsonify({'error': 'User ID is required'}), 400

        if not data.get('username'):
            return jsonify({'error': 'Username is required'}), 400

        if not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400

        # Add the collaborator
        success, error = problem_instance_service.add_collaborator(instance_id, data)

        if not success:
            return jsonify({'error': error or 'Failed to add collaborator'}), 400

        return jsonify({'message': 'Collaborator added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@problem_instance_blueprint.route('/problem-instances/<instance_id>/subtasks', methods=['POST'])
def create_subtask_instance(instance_id):
    """
    Create a subtask instance.

    Request body should contain:
    - stepNum: The step number
    - assignee: Object with userId and username
    - reporter: Object with userId and username
    - status: The status of the subtask

    Returns:
        JSON response with success message and subtask ID, or error
    """
    try:
        data = request.get_json()

        # Validate required fields
        if 'stepNum' not in data:
            return jsonify({'error': 'Step number is required'}), 400

        # Create the subtask instance
        subtask_id, error = subtask_instance_service.create_subtask_instance(instance_id, data)

        if error:
            return jsonify({'error': error}), 400

        return jsonify({
            'message': 'Subtask instance created successfully',
            'subtaskId': subtask_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@problem_instance_blueprint.route('/problem-instances/<instance_id>', methods=['PATCH'])
def update_problem_instance(instance_id):
    """
    Update a problem instance.

    Request body can contain any fields to update, including:
    - status: The new status
    - completedAt: Timestamp when the problem was completed
    - collaborationMode: 'solo' or 'pair'

    Returns:
        JSON response with success message or error
    """
    try:
        data = request.get_json()

        # Check if this is a status-only update (for backward compatibility)
        if 'status' in data and len(data) <= 2 and ('completedAt' in data or len(data) == 1):
            # Use the original status update method
            success, error = problem_instance_service.update_problem_instance_status(
                instance_id,
                data['status'],
                data.get('completedAt')
            )
        else:
            # Use the new general update method
            success, error = problem_instance_service.update_problem_instance(
                instance_id,
                data
            )

        if not success:
            return jsonify({'error': error or 'Failed to update problem instance'}), 400

        return jsonify({'message': 'Problem instance updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500