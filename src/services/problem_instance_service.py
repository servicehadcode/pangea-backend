from typing import List, Optional, Tuple, Dict, Any
from pymongo import MongoClient
from pymongo.results import InsertOneResult, UpdateResult
from bson import ObjectId
from models.problem_instance import ProblemInstance
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ProblemInstanceService:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('MONGODB_DB')]
        self.collection = self.db.problem_instances

    def get_problem_instance(self, problem_num: str, user_id: str) -> Optional[ProblemInstance]:
        """
        Get a specific problem instance for a user and problem.

        Args:
            problem_num: The problem number
            user_id: The user ID

        Returns:
            ProblemInstance object if found, None otherwise
        """
        instance = self.collection.find_one({
            'problemNum': problem_num,
            'owner.userId': user_id
        })
        if instance:
            # Convert ObjectId to string for serialization
            instance['_id'] = str(instance['_id'])
            return ProblemInstance.from_dict(instance)
        return None

    def get_problem_instance_by_id(self, instance_id: str) -> Optional[ProblemInstance]:
        """
        Get a problem instance by its ID.

        Args:
            instance_id: The problem instance ID

        Returns:
            ProblemInstance object if found, None otherwise
        """
        try:
            instance = self.collection.find_one({'_id': ObjectId(instance_id)})
            if instance:
                # Convert ObjectId to string for serialization
                instance['_id'] = str(instance['_id'])
                return ProblemInstance.from_dict(instance)
            return None
        except Exception:
            return None

    def get_collaborators(self, instance_id: str) -> List[dict]:
        """
        Get all collaborators for a problem instance.

        Args:
            instance_id: The problem instance ID

        Returns:
            List of collaborator dictionaries
        """
        try:
            instance = self.collection.find_one({'_id': ObjectId(instance_id)})
            if instance:
                collaborators = instance.get('collaborators', [])
                # Process any ObjectId fields in collaborators if needed
                for collab in collaborators:
                    if '_id' in collab and isinstance(collab['_id'], ObjectId):
                        collab['_id'] = str(collab['_id'])
                return collaborators
            return []
        except Exception as e:
            print(f"Error getting collaborators: {str(e)}")
            return []

    def create_problem_instance(self, problem_instance_data: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """
        Create a new problem instance.

        Args:
            problem_instance_data: Dictionary containing problem instance data

        Returns:
            Tuple of (instance_id, error_message)
        """
        try:
            # Check if an instance already exists for this user and problem
            existing = self.collection.find_one({
                'problemNum': problem_instance_data.get('problemNum'),
                'owner.userId': problem_instance_data.get('owner', {}).get('userId')
            })

            if existing:
                return None, "Problem instance already exists for this user and problem"

            # Set timestamps
            now = datetime.now().isoformat()
            problem_instance_data['startedAt'] = now
            problem_instance_data['lastUpdatedAt'] = now
            problem_instance_data['status'] = problem_instance_data.get('status', 'in-progress')

            # Create the instance
            result: InsertOneResult = self.collection.insert_one(problem_instance_data)
            return str(result.inserted_id), None

        except Exception as e:
            print(f"Error creating problem instance: {str(e)}")
            return None, str(e)

    def add_collaborator(self, instance_id: str, collaborator_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Add a collaborator to a problem instance.

        Args:
            instance_id: The problem instance ID
            collaborator_data: Dictionary containing collaborator data

        Returns:
            Tuple of (success, error_message)
        """
        try:
            # Check if the instance exists
            instance = self.collection.find_one({'_id': ObjectId(instance_id)})
            if not instance:
                return False, "Problem instance not found"

            # Check if the collaborator already exists
            collaborators = instance.get('collaborators', [])
            for collab in collaborators:
                if collab.get('userId') == collaborator_data.get('userId'):
                    return False, "Collaborator already exists in this problem instance"

            # Add timestamps
            now = datetime.now().isoformat()
            collaborator_data['invitedAt'] = now
            collaborator_data['status'] = 'invited'

            # Add the collaborator
            result: UpdateResult = self.collection.update_one(
                {'_id': ObjectId(instance_id)},
                {
                    '$push': {'collaborators': collaborator_data},
                    '$set': {'lastUpdatedAt': now}
                }
            )

            return result.modified_count > 0, None

        except Exception as e:
            print(f"Error adding collaborator: {str(e)}")
            return False, str(e)

    def update_problem_instance_status(self, instance_id: str, status: str, completed_at: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """
        Update the status of a problem instance.

        Args:
            instance_id: The problem instance ID
            status: The new status
            completed_at: Timestamp when the problem was completed (optional)

        Returns:
            Tuple of (success, error_message)
        """
        try:
            # Check if the instance exists
            instance = self.collection.find_one({'_id': ObjectId(instance_id)})
            if not instance:
                return False, "Problem instance not found"

            # Prepare update data
            update_data = {
                'status': status,
                'lastUpdatedAt': datetime.now().isoformat()
            }

            # Add completedAt if provided or if status is 'completed'
            if completed_at:
                update_data['completedAt'] = completed_at
            elif status == 'completed' and not instance.get('completedAt'):
                update_data['completedAt'] = datetime.now().isoformat()

            # Update the instance
            result: UpdateResult = self.collection.update_one(
                {'_id': ObjectId(instance_id)},
                {'$set': update_data}
            )

            return result.modified_count > 0, None

        except Exception as e:
            print(f"Error updating problem instance status: {str(e)}")
            return False, str(e)
