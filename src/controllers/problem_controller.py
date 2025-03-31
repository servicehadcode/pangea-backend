from flask import Blueprint, request, jsonify
from services.problem_service import ProblemService
from models.problem import Problem

problem_blueprint = Blueprint('problem', __name__)
problem_service = ProblemService()

@problem_blueprint.route('/problems', methods=['GET'])
def get_problems():
    try:
        category = request.args.get('category')
        problems = problem_service.get_all_problems(category)
        return jsonify([problem.to_dict() for problem in problems]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@problem_blueprint.route('/problem/<problem_num>', methods=['GET'])
def get_problem(problem_num):
    try:
        problem = problem_service.get_problem_by_num(problem_num)
        if not problem:
            return jsonify({'error': 'Problem not found'}), 404
        return jsonify(problem.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@problem_blueprint.route('/addProblem', methods=['POST'])
def add_problem():
    try:
        data = request.get_json()
        problem = Problem.from_dict(data)
        if problem_service.add_problem(problem):
            return jsonify({'message': 'Problem added successfully'}), 201
        return jsonify({'error': 'Problem number already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@problem_blueprint.route('/updateProblem/<problem_num>', methods=['PUT'])
def update_problem(problem_num):
    try:
        data = request.get_json()
        if problem_service.update_problem(problem_num, data):
            return jsonify({'message': 'Problem updated successfully'}), 200
        return jsonify({'error': 'Problem not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@problem_blueprint.route('/deleteProblem/<problem_num>', methods=['DELETE'])
def delete_problem(problem_num):
    try:
        if problem_service.delete_problem(problem_num):
            return jsonify({'message': 'Problem deleted successfully'}), 200
        return jsonify({'error': 'Problem not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500