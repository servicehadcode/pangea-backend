from flask import Blueprint, request, jsonify
from services.subtask_instance_service import SubtaskInstanceService
from bson import ObjectId

subtask_instance_blueprint = Blueprint('subtask_instance', __name__)
subtask_instance_service = SubtaskInstanceService()

@subtask_instance_blueprint.route('/subtask-instances/<subtask_id>', methods=['GET'])
def get_subtask_instance(subtask_id):
    """
    Get a specific subtask instance by ID.

    Args:
        subtask_id: The subtask instance ID

    Returns:
        JSON response with subtask instance data or error
    """
    try:
        subtask = subtask_instance_service.get_subtask_instance(subtask_id)
        if not subtask:
            return jsonify({'error': 'Subtask instance not found'}), 404
        return jsonify(subtask.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subtask_instance_blueprint.route('/problem-instances/<instance_id>/subtasks/<subtask_id>', methods=['PATCH'])
def update_subtask_instance(instance_id, subtask_id):
    """
    Update a subtask instance.

    Request body can contain:
    - assignee: Object with userId and username
    - reporter: Object with userId and username
    - status: The status of the subtask
    - branchCreated: Whether a branch was created
    - prCreated: Whether a PR was created
    - deliverables: Comments/notes provided by the assignee
    - completedAt: Timestamp when the subtask was completed

    Returns:
        JSON response with success message or error
    """
    try:
        data = request.get_json()

        # Verify the subtask belongs to the specified problem instance
        subtask = subtask_instance_service.get_subtask_instance(subtask_id)
        if not subtask:
            return jsonify({'error': 'Subtask instance not found'}), 404

        if subtask.problem_instance_id != instance_id:
            return jsonify({'error': 'Subtask does not belong to the specified problem instance'}), 400

        # Update the subtask
        success, error = subtask_instance_service.update_subtask_instance(subtask_id, data)

        if not success:
            return jsonify({'error': error or 'Failed to update subtask instance'}), 400

        return jsonify({'message': 'Subtask instance updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@subtask_instance_blueprint.route('/problem-instances/<instance_id>/subtasks/<subtask_id>/criteria/<criteria_id>', methods=['PATCH'])
def update_acceptance_criteria(instance_id, subtask_id, criteria_id):
    """
    Update the status of a specific acceptance criterion.

    Request body should contain:
    - completed: Whether the criterion is completed

    Returns:
        JSON response with success message or error
    """
    try:
        data = request.get_json()

        # Validate required fields
        if 'completed' not in data:
            return jsonify({'error': 'Completed status is required'}), 400

        # Verify the subtask belongs to the specified problem instance
        subtask = subtask_instance_service.get_subtask_instance(subtask_id)
        if not subtask:
            return jsonify({'error': 'Subtask instance not found'}), 404

        if subtask.problem_instance_id != instance_id:
            return jsonify({'error': 'Subtask does not belong to the specified problem instance'}), 400

        # Update the acceptance criterion
        success, error = subtask_instance_service.update_acceptance_criteria(
            subtask_id,
            criteria_id,
            data['completed']
        )

        if not success:
            return jsonify({'error': error or 'Failed to update acceptance criterion'}), 400

        return jsonify({'message': 'Acceptance criterion updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
