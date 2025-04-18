from datetime import datetime
from typing import List, Dict, Optional, Any

class ProblemInstance:
    def __init__(self,
                 problem_num: str,
                 owner: Dict,
                 collaboration_mode: str,
                 collaborators: List[Dict] = None,
                 status: str = "in-progress",
                 started_at: Optional[datetime] = None,
                 last_updated_at: Optional[datetime] = None,
                 completed_at: Optional[datetime] = None,
                 collaboration_details: Optional[Dict[str, Any]] = None,
                 _id: str = None):
        self.problem_num = problem_num
        self.owner = owner
        self.collaboration_mode = collaboration_mode
        self.collaborators = collaborators or []
        self.status = status
        self.started_at = started_at or datetime.now()
        self.last_updated_at = last_updated_at or datetime.now()
        self.completed_at = completed_at
        self.collaboration_details = collaboration_details or {}
        self._id = _id

    def to_dict(self) -> Dict:
        """Convert the problem instance object to a dictionary."""
        return {
            'problemNum': self.problem_num,
            'owner': self.owner,
            'collaborationMode': self.collaboration_mode,
            'collaborators': self.collaborators,
            'status': self.status,
            'startedAt': self.started_at.isoformat() if self.started_at else None,
            'lastUpdatedAt': self.last_updated_at.isoformat() if self.last_updated_at else None,
            'completedAt': self.completed_at.isoformat() if self.completed_at else None,
            'collaborationDetails': self.collaboration_details,
            '_id': self._id
        }

    @staticmethod
    def from_dict(data: Dict) -> 'ProblemInstance':
        """Create a ProblemInstance object from a dictionary."""
        # Parse datetime fields
        started_at = None
        if 'startedAt' in data:
            try:
                started_at = datetime.fromisoformat(data['startedAt'])
            except (ValueError, TypeError):
                started_at = datetime.now()

        last_updated_at = None
        if 'lastUpdatedAt' in data:
            try:
                last_updated_at = datetime.fromisoformat(data['lastUpdatedAt'])
            except (ValueError, TypeError):
                last_updated_at = datetime.now()

        completed_at = None
        if 'completedAt' in data and data['completedAt']:
            try:
                completed_at = datetime.fromisoformat(data['completedAt'])
            except (ValueError, TypeError):
                completed_at = None

        return ProblemInstance(
            problem_num=data.get('problemNum'),
            owner=data.get('owner', {}),
            collaboration_mode=data.get('collaborationMode', 'solo'),
            collaborators=data.get('collaborators', []),
            status=data.get('status', 'in-progress'),
            started_at=started_at,
            last_updated_at=last_updated_at,
            completed_at=completed_at,
            collaboration_details=data.get('collaborationDetails', {}),
            _id=data.get('_id')
        )
