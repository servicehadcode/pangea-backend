from datetime import datetime
from typing import List, Dict, Optional

class Problem:
    def __init__(self, problem_num: str, title: str, description: str, long_description: str,
                 difficulty: str, category: str, requirements: Dict, tags: List[str],
                 steps: List[Dict], resources: List[Dict], metadata: Dict,
                 downloadable_items: List[str] = None, preparation_steps: List[str] = None):
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
        self.downloadable_items = downloadable_items or []
        self.preparation_steps = preparation_steps or []

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
            'metadata': self.metadata,
            'downloadableItems': self.downloadable_items,
            'preparationSteps': self.preparation_steps
        }

    @staticmethod
    def from_dict(data: Dict):
        # Process steps to ensure they have the required fields
        steps = data.get('steps', [])
        for step in steps:
            if 'details' not in step:
                step['details'] = []
            if 'acceptanceCriteria' not in step:
                step['acceptanceCriteria'] = []

        # Process metadata to ensure it has the 'gitRepo' field
        metadata = data.get('metadata', {})
        if 'gitRepo' not in metadata:
            metadata['gitRepo'] = ''

        # Handle legacy data that might have acceptanceCriteria at the root level
        # If found, distribute it to all steps
        root_acceptance_criteria = data.get('acceptanceCriteria', [])
        if root_acceptance_criteria and steps:
            # If there are root-level acceptance criteria, add them to each step
            for step in steps:
                if not step.get('acceptanceCriteria'):
                    step['acceptanceCriteria'] = root_acceptance_criteria
                else:
                    # Merge with existing criteria, avoiding duplicates
                    existing = set(step['acceptanceCriteria'])
                    for criterion in root_acceptance_criteria:
                        if criterion not in existing:
                            step['acceptanceCriteria'].append(criterion)

        return Problem(
            problem_num=data.get('problem_num'),
            title=data.get('title'),
            description=data.get('description'),
            long_description=data.get('longDescription'),
            difficulty=data.get('difficulty'),
            category=data.get('category'),
            requirements=data.get('requirements', {}),
            tags=data.get('tags', []),
            steps=steps,
            resources=data.get('resources', []),
            metadata=metadata,
            downloadable_items=data.get('downloadableItems', []),
            preparation_steps=data.get('preparationSteps', [])
        )