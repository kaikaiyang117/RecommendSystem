from neo4j import GraphDatabase
from User import User
from Activity import Activity
from datetime import datetime
from typing import List

class Neo4jDatabase:
    def __init__(self, uri: str, username: str, password: str):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        """关闭连接"""
        self.driver.close()

    def create_user_node(self, user: User):
        """将User对象转化为Neo4j的节点"""
        with self.driver.session() as session:
            session.write_transaction(self._create_user, user)

    @staticmethod
    def _create_user(tx, user: User):
        """创建用户节点的实际查询"""
        query = (
            "CREATE (u:User {user_id: $user_id, name: $name, email: $email, major: $major, "
            "college: $college, tags: $tags, participation_count: $participation_count, "
            "joined_activities: $joined_activities, created_at: $created_at, updated_at: $updated_at})"
        )
        tx.run(query, 
               user_id=user.user_id, 
               name=user.name,
               email=user.email,
               major=user.major,
               college=user.college,
               tags=user.tags,
               participation_count=user.participation_count,
               joined_activities=user.joined_activities,
               created_at=user.created_at,
               updated_at=user.updated_at)

    def create_activity_node(self, activity: Activity):
        """将Activity对象转化为Neo4j的节点"""
        with self.driver.session() as session:
            session.write_transaction(self._create_activity, activity)

    @staticmethod
    def _create_activity(tx, activity: Activity):
        """创建活动节点的实际查询"""
        query = (
            "CREATE (a:Activity {activity_id: $activity_id, title: $title, description: $description, "
            "sponsor: $sponsor, tags: $tags, date: $date, location: $location, duration: $duration, "
            "audience: $audience, capacity: $capacity, current_participants: $current_participants, "
            "organizer: $organizer, created_at: $created_at, updated_at: $updated_at, img_url: $img_url})"
        )
        tx.run(query, 
               activity_id=activity.activity_id, 
               title=activity.title,
               description=activity.description,
               sponsor=activity.sponsor,
               tags=activity.tags,
               date=activity.date.isoformat(),
               location=activity.location,
               duration=activity.duration,
               audience=activity.audience,
               capacity=activity.capacity,
               current_participants=activity.current_participants,
               organizer=activity.organizer,
               created_at=activity.created_at,
               updated_at=activity.updated_at,
               img_url=activity.img_url)

    def create_participation_relationship(self, user: User, activity: Activity):
        """创建用户与活动之间的参与关系"""
        with self.driver.session() as session:
            session.write_transaction(self._create_participation, user, activity)

    @staticmethod
    def _create_participation(tx, user: User, activity: Activity):
        """创建用户和活动之间的参与关系"""
        query = (
            "MATCH (u:User {user_id: $user_id}), (a:Activity {activity_id: $activity_id}) "
            "CREATE (u)-[:PARTICIPATED_IN]->(a)"
        )
        tx.run(query, user_id=user.user_id, activity_id=activity.activity_id)

# 示例用法
if __name__ == "__main__":
    # 创建User对象
    user = User(
        user_id="12345",
        name="Alice",
        email="alice@example.com",
        major="Computer Science",
        college="Engineering",
        tags=["AI", "Robotics"],
        participation_count=3,
        joined_activities=["activity_1", "activity_2"],
        created_at="2024-12-02",
        updated_at="2024-12-02"
    )

    # 创建Activity对象
    activity = Activity(
        activity_id="activity_001",
        title="AI Workshop",
        description="A workshop on AI and machine learning.",
        sponsor="TechClub",
        tags=["AI", "Machine Learning", "Workshop"],
        date=datetime(2024, 12, 10, 10, 0),
        location="Room 101, Engineering Building",
        duration=120,
        audience="Undergraduate students",
        capacity=50,
        current_participants=10,
        organizer="Tech Club",
        img_url="https://example.com/image.jpg"
    )

    # 连接到Neo4j数据库并创建节点
    db = Neo4jDatabase(uri="bolt://localhost:7687", username="neo4j", password="kkykkykky")
    
    # 创建用户节点
    db.create_user_node(user)
    
    # 创建活动节点
    db.create_activity_node(activity)
    
    # 创建用户参与活动的关系
    db.create_participation_relationship(user, activity)
    
    db.close()

    print("User and Activity nodes created in Neo4j and relationship established.")
