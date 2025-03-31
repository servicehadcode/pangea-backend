from datetime import datetime
from typing import List, Dict, Optional

class Problem:
    def __init__(self, problem_num: str, title: str, description: str, long_description: str,
                 difficulty: str, category: str, requirements: Dict, tags: List[str],
                 steps: List[Dict], resources: List[Dict], metadata: Dict):
        self.problem_num = problem_num
        self.title = title
        self.description = description
        self.long_description = long_description
        self.difficulty = difficulty
        self.category = category
        self.requirements = requirements
        self.tags = tags
        self.steps = steps
        self.resources = resources
        self.metadata = metadata

    def to_dict(self):
        return {
            'problem_num': self.problem_num,
            'title': self.title,
            'description': self.description,
            'longDescription': self.long_description,
            'difficulty': self.difficulty,
            'category': self.category,
            'requirements': self.requirements,
            'tags': self.tags,
            'steps': self.steps,
            'resources': self.resources,
            'metadata': self.metadata
        }

    @staticmethod
    def from_dict(data: Dict):
        return Problem(
            problem_num=data.get('problem_num'),
            title=data.get('title'),
            description=data.get('description'),
            long_description=data.get('longDescription'),
            difficulty=data.get('difficulty'),
            category=data.get('category'),
            requirements=data.get('requirements', {}),
            tags=data.get('tags', []),
            steps=data.get('steps', []),
            resources=data.get('resources', []),
            metadata=data.get('metadata', {})
        )