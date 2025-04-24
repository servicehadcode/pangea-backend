from typing import List, Dict, Optional, Tuple, Any
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv
from models.discussion import Discussion

load_dotenv()

class DiscussionService:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('MONGODB_DB')]
        self.collection = self.db.discussions

    def create_discussion(self, discussion: Discussion) -> Tuple[Optional[str], Optional[str]]:
        """
        Create a new discussion or reply.

        Args:
            discussion: The Discussion object to create

        Returns:
            Tuple of (discussion_id, error_message)
        """
        try:
            # Insert the discussion
            result = self.collection.insert_one(discussion.to_dict())
            return str(result.inserted_id), None
        except Exception as e:
            return None, str(e)

    def get_discussions_by_problem_id(self, problem_id: str) -> List[Discussion]:
        """
        Get all discussions for a specific problem.

        Args:
            problem_id: The problem ID

        Returns:
            List of Discussion objects
        """
        try:
            # Get all top-level discussions (no parentId)
            discussions = self.collection.find({
                'problemId': problem_id,
                'parentId': None
            })
            
            result = []
            for discussion in discussions:
                # Convert ObjectId to string for serialization
                discussion['_id'] = str(discussion['_id'])
                
                # Get replies for this discussion
                replies = self.get_replies(str(discussion['_id']))
                
                # Create Discussion object
                discussion_obj = Discussion.from_dict(discussion)
                
                # Add to result with replies
                result.append({
                    **discussion_obj.to_dict(),
                    'replies': [reply.to_dict() for reply in replies]
                })
                
            return result
        except Exception as e:
            print(f"Error getting discussions: {str(e)}")
            return []

    def get_replies(self, parent_id: str) -> List[Discussion]:
        """
        Get all replies for a discussion.

        Args:
            parent_id: The parent discussion ID

        Returns:
            List of Discussion objects
        """
        try:
            replies = self.collection.find({'parentId': parent_id})
            result = []
            for reply in replies:
                # Convert ObjectId to string for serialization
                reply['_id'] = str(reply['_id'])
                result.append(Discussion.from_dict(reply))
            return result
        except Exception:
            return []

    def add_vote(self, discussion_id: str) -> bool:
        """
        Add a vote to a discussion.

        Args:
            discussion_id: The discussion ID

        Returns:
            True if successful, False otherwise
        """
        try:
            # Increment the votes field
            result = self.collection.update_one(
                {'_id': ObjectId(discussion_id)},
                {'$inc': {'votes': 1}}
            )
            return result.modified_count > 0
        except Exception:
            return False

    def get_discussion_by_id(self, discussion_id: str) -> Optional[Discussion]:
        """
        Get a discussion by its ID.

        Args:
            discussion_id: The discussion ID

        Returns:
            Discussion object if found, None otherwise
        """
        try:
            discussion = self.collection.find_one({'_id': ObjectId(discussion_id)})
            if discussion:
                # Convert ObjectId to string for serialization
                discussion['_id'] = str(discussion['_id'])
                return Discussion.from_dict(discussion)
            return None
        except Exception:
            return None
