from datetime import datetime
from typing import List

class User:
    def __init__(self, user_id: str, name: str, email: str, major: str, college: str,
                 tags: List[str], participation_count: int = 0, joined_activities: List[str] = None,
                 created_at: str = None, updated_at: str = None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.major = major
        self.college = college
        self.tags = tags
        self.participation_count = participation_count
        self.joined_activities = joined_activities if joined_activities else []
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"User(user_id='{self.user_id}', name='{self.name}', email='{self.email}', major='{self.major}', college='{self.college}', tags={self.tags}, participation_count={self.participation_count})"
