from datetime import datetime
from typing import Dict, List, Optional, Any

class Discussion:
    def __init__(self,
                 problem_id: str,
                 content: str,
                 user_id: str,
                 parent_id: Optional[str] = None,
                 votes: int = 0,
                 created_at: Optional[datetime] = None,
                 _id: Optional[str] = None):
        self.problem_id = problem_id
        self.content = content
        self.user_id = user_id
        self.parent_id = parent_id
        self.votes = votes
        self.created_at = created_at or datetime.now()
        self._id = _id

    def to_dict(self) -> Dict[str, Any]:
        """Convert the discussion object to a dictionary."""
        result = {
            'problemId': self.problem_id,
            'content': self.content,
            'userId': self.user_id,
            'parentId': self.parent_id,
            'votes': self.votes,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

        # Only include _id if it's not None
        if self._id is not None:
            result['_id'] = self._id

        return result

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Discussion':
        """Create a Discussion object from a dictionary."""
        created_at = None
        if 'createdAt' in data:
            try:
                created_at = datetime.fromisoformat(data['createdAt'])
            except (ValueError, TypeError):
                created_at = datetime.now()

        return Discussion(
            problem_id=data.get('problemId'),
            content=data.get('content'),
            user_id=data.get('userId'),
            parent_id=data.get('parentId'),
            votes=data.get('votes', 0),
            created_at=created_at,
            _id=data.get('_id')
        )
