from typing import List, Optional
from pymongo import MongoClient
from models.problem import Problem
import os
from dotenv import load_dotenv

load_dotenv()

class ProblemService:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('MONGODB_DB')]
        self.collection = self.db.problems

    def get_all_problems(self, category: Optional[str] = None) -> List[Problem]:
        query = {'category': category} if category else {}
        problems = self.collection.find(query)
        return [Problem.from_dict(problem) for problem in problems]

    def get_problem_by_num(self, problem_num: str) -> Optional[Problem]:
        problem = self.collection.find_one({'problem_num': problem_num})
        return Problem.from_dict(problem) if problem else None

    def add_problem(self, problem: Problem) -> bool:
        # Check if problem number already exists
        if self.collection.find_one({'problem_num': problem.problem_num}):
            return False
        
        self.collection.insert_one(problem.to_dict())
        return True

    def update_problem(self, problem_num: str, updated_data: dict) -> bool:
        result = self.collection.update_one(
            {'problem_num': problem_num},
            {'$set': updated_data}
        )
        return result.modified_count > 0

    def delete_problem(self, problem_num: str) -> bool:
        result = self.collection.delete_one({'problem_num': problem_num})
        return result.deleted_count > 0