from typing import List, Optional, Tuple, Dict, Any
from pymongo import MongoClient
from pymongo.results import InsertOneResult, UpdateResult
from bson import ObjectId
from models.subtask_instance import SubtaskInstance
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class SubtaskInstanceService:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('MONGODB_DB')]
        self.collection = self.db.subtask_instances

    def get_subtask_instances(self, problem_instance_id: str) -> List[SubtaskInstance]:
        """
        Get all subtask instances for a problem instance.

        Args:
            problem_instance_id: The problem instance ID

        Returns:
            List of SubtaskInstance objects
        """
        try:
            subtasks = self.collection.find({'problemInstanceId': problem_instance_id})
            result = []
            for subtask in subtasks:
                # Convert ObjectId to string for serialization
                subtask['_id'] = str(subtask['_id'])
                result.append(SubtaskInstance.from_dict(subtask))
            return result
        except Exception:
            return []

    def get_subtask_instance(self, subtask_id: str) -> Optional[SubtaskInstance]:
        """
        Get a specific subtask instance by ID.

        Args:
            subtask_id: The subtask instance ID

        Returns:
            SubtaskInstance object if found, None otherwise
        """
        try:
            subtask = self.collection.find_one({'_id': ObjectId(subtask_id)})
            if subtask:
                # Convert ObjectId to string for serialization
                subtask['_id'] = str(subtask['_id'])
                return SubtaskInstance.from_dict(subtask)
            return None
        except Exception:
            return None

    def create_subtask_instance(self, problem_instance_id: str, subtask_data: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """
        Create a new subtask instance.

        Args:
            problem_instance_id: The problem instance ID
            subtask_data: Dictionary containing subtask data

        Returns:
            Tuple of (subtask_id, error_message)
        """
        try:
            # Check if the problem instance exists
            from services.problem_instance_service import ProblemInstanceService
            problem_instance_service = ProblemInstanceService()
            problem_instance = problem_instance_service.get_problem_instance_by_id(problem_instance_id)

            if not problem_instance:
                return None, "Problem instance not found"

            # Check if a subtask with this step number already exists
            existing = self.collection.find_one({
                'problemInstanceId': problem_instance_id,
                'stepNum': subtask_data.get('stepNum')
            })

            if existing:
                return None, f"Subtask for step {subtask_data.get('stepNum')} already exists"

            # Add problem instance ID and timestamps
            subtask_data['problemInstanceId'] = problem_instance_id
            if subtask_data.get('status') == 'in-progress':
                subtask_data['startedAt'] = datetime.now().isoformat()

            # Create the subtask
            result: InsertOneResult = self.collection.insert_one(subtask_data)
            return str(result.inserted_id), None

        except Exception as e:
            print(f"Error creating subtask instance: {str(e)}")
            return None, str(e)

    def update_subtask_instance(self, subtask_id: str, update_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Update a subtask instance.

        Args:
            subtask_id: The subtask instance ID
            update_data: Dictionary containing fields to update

        Returns:
            Tuple of (success, error_message)
        """
        try:
            # Check if the subtask exists
            subtask = self.get_subtask_instance(subtask_id)
            if not subtask:
                return False, "Subtask instance not found"

            # Handle status changes and timestamps
            if 'status' in update_data:
                # If changing to in-progress and no startedAt, set it
                if update_data['status'] == 'in-progress' and not subtask.started_at:
                    update_data['startedAt'] = datetime.now().isoformat()
                # If changing to completed and no completedAt provided, set it
                elif update_data['status'] == 'completed' and not update_data.get('completedAt'):
                    update_data['completedAt'] = datetime.now().isoformat()

            # Update the subtask
            result: UpdateResult = self.collection.update_one(
                {'_id': ObjectId(subtask_id)},
                {'$set': update_data}
            )

            return result.modified_count > 0, None

        except Exception as e:
            print(f"Error updating subtask instance: {str(e)}")
            return False, str(e)

    def update_acceptance_criteria(self, subtask_id: str, criteria_id: str, completed: bool) -> Tuple[bool, Optional[str]]:
        """
        Update the status of a specific acceptance criterion.

        Args:
            subtask_id: The subtask instance ID
            criteria_id: The ID or index of the criterion
            completed: Whether the criterion is completed

        Returns:
            Tuple of (success, error_message)
        """
        try:
            # Check if the subtask exists
            subtask = self.get_subtask_instance(subtask_id)
            if not subtask:
                return False, "Subtask instance not found"

            # Find the criterion by ID or index
            try:
                # Try to use criteria_id as an index
                index = int(criteria_id)
                if index < 0 or index >= len(subtask.acceptance_criteria):
                    return False, f"Acceptance criterion index {index} out of range"

                # Update the criterion at the specified index
                result: UpdateResult = self.collection.update_one(
                    {'_id': ObjectId(subtask_id)},
                    {'$set': {f'acceptanceCriteria.{index}.completed': completed}}
                )

            except ValueError:
                # criteria_id is not an index, try to find by criteriaText
                found = False
                for i, criterion in enumerate(subtask.acceptance_criteria):
                    if criterion.get('criteriaText') == criteria_id:
                        result: UpdateResult = self.collection.update_one(
                            {'_id': ObjectId(subtask_id)},
                            {'$set': {f'acceptanceCriteria.{i}.completed': completed}}
                        )
                        found = True
                        break

                if not found:
                    return False, f"Acceptance criterion '{criteria_id}' not found"

            return True, None

        except Exception as e:
            print(f"Error updating acceptance criterion: {str(e)}")
            return False, str(e)
