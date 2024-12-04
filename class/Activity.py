from datetime import datetime
from typing import List

class Activity:
    def __init__(self, activity_id: str, title: str, description: str, sponsor: str,
                 tags: List[str], date: datetime, location: str, duration: int, audience: str,
                 capacity: int, current_participants: int = 0, organizer: str = "",
                 created_at: str = None, updated_at: str = None, img_url: str = ""):
        self.activity_id = activity_id
        self.title = title
        self.description = description
        self.sponsor = sponsor
        self.tags = tags
        self.date = date
        self.location = location
        self.duration = duration
        self.audience = audience
        self.capacity = capacity
        self.current_participants = current_participants
        self.organizer = organizer
        self.created_at = created_at if created_at else datetime.now().isoformat()
        self.updated_at = updated_at if updated_at else datetime.now().isoformat()
        self.img_url = img_url

    def __repr__(self):
        return (f"Activity(activity_id='{self.activity_id}', title='{self.title}', "
                f"description='{self.description}', sponsor='{self.sponsor}', "
                f"tags={self.tags}, date={self.date}, location='{self.location}', "
                f"duration={self.duration}, audience='{self.audience}', capacity={self.capacity}, "
                f"current_participants={self.current_participants}, organizer='{self.organizer}', "
                f"created_at={self.created_at}, updated_at={self.updated_at}, img_url='{self.img_url}')")
