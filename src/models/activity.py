from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Activity(BaseModel):
    username: str
    email: str
    action: str  # "signup", "login", "logout", etc.
    timestamp: datetime
    avatar: Optional[str] = None

