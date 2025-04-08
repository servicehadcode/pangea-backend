from datetime import datetime
from typing import List, Dict, Optional

class SubtaskInstance:
    def __init__(self,
                 problem_instance_id: str,
                 step_num: int,
                 assignee: Dict = None,
                 reporter: Dict = None,
                 status: str = "not-started",
                 branch_created: bool = False,
                 pr_created: bool = False,
                 deliverables: str = "",
                 acceptance_criteria: List[Dict] = None,
                 pr_feedback: List[Dict] = None,
                 started_at: Optional[datetime] = None,
                 completed_at: Optional[datetime] = None,
                 _id: str = None):
        self.problem_instance_id = problem_instance_id
        self.step_num = step_num
        self.assignee = assignee or {}
        self.reporter = reporter or {}
        self.status = status
        self.branch_created = branch_created
        self.pr_created = pr_created
        self.deliverables = deliverables
        self.acceptance_criteria = acceptance_criteria or []
        self.pr_feedback = pr_feedback or []
        self.started_at = started_at
        self.completed_at = completed_at
        self._id = _id

    def to_dict(self) -> Dict:
        """Convert the subtask instance object to a dictionary."""
        return {
            'problemInstanceId': self.problem_instance_id,
            'stepNum': self.step_num,
            'assignee': self.assignee,
            'reporter': self.reporter,
            'status': self.status,
            'branchCreated': self.branch_created,
            'prCreated': self.pr_created,
            'deliverables': self.deliverables,
            'acceptanceCriteria': self.acceptance_criteria,
            'prFeedback': self.pr_feedback,
            'startedAt': self.started_at.isoformat() if self.started_at else None,
            'completedAt': self.completed_at.isoformat() if self.completed_at else None,
            '_id': self._id
        }

    @staticmethod
    def from_dict(data: Dict) -> 'SubtaskInstance':
        """Create a SubtaskInstance object from a dictionary."""
        # Parse datetime fields
        started_at = None
        if 'startedAt' in data and data['startedAt']:
            try:
                started_at = datetime.fromisoformat(data['startedAt'])
            except (ValueError, TypeError):
                started_at = None
                
        completed_at = None
        if 'completedAt' in data and data['completedAt']:
            try:
                completed_at = datetime.fromisoformat(data['completedAt'])
            except (ValueError, TypeError):
                completed_at = None
                
        return SubtaskInstance(
            problem_instance_id=data.get('problemInstanceId'),
            step_num=data.get('stepNum'),
            assignee=data.get('assignee', {}),
            reporter=data.get('reporter', {}),
            status=data.get('status', 'not-started'),
            branch_created=data.get('branchCreated', False),
            pr_created=data.get('prCreated', False),
            deliverables=data.get('deliverables', ''),
            acceptance_criteria=data.get('acceptanceCriteria', []),
            pr_feedback=data.get('prFeedback', []),
            started_at=started_at,
            completed_at=completed_at,
            _id=data.get('_id')
        )
