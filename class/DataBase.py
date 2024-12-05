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

    def create_participation_relationship(self, user: User, activity: Activity, rating: int, comments: str):
        """创建用户与活动之间的参与关系，并添加评分和评论"""
        with self.driver.session() as session:
            session.write_transaction(self._create_participation, user, activity, rating, comments)

    @staticmethod
    def _create_participation(tx, user: User, activity: Activity, rating: int, comments: str):
        """创建用户和活动之间的参与关系并添加评分和评论"""
        query = (
            "MATCH (u:User {user_id: $user_id}), (a:Activity {activity_id: $activity_id}) "
            "CREATE (u)-[r:PARTICIPATED_IN {rating: $rating, comments: $comments}]->(a)"
        )
        tx.run(query, 
               user_id=user.user_id, 
               activity_id=activity.activity_id, 
               rating=rating, 
               comments=comments)

    # 创建用户对活动感兴趣的关系
    def create_interested_in_relationship(self, user: User, activity: Activity, interest_level: str):
        """用户对某个活动表示感兴趣"""
        with self.driver.session() as session:
            session.write_transaction(self._create_interested_in, user, activity, interest_level)

    @staticmethod
    def _create_interested_in(tx, user: User, activity: Activity, interest_level: str):
        """创建用户对活动感兴趣的关系"""
        query = (
            "MATCH (u:User {user_id: $user_id}), (a:Activity {activity_id: $activity_id}) "
            "CREATE (u)-[r:INTERESTED_IN {interest_level: $interest_level}]->(a)"
        )
        tx.run(query, 
               user_id=user.user_id, 
               activity_id=activity.activity_id, 
               interest_level=interest_level)

    # 创建用户是活动主办方的关系
    def create_organizes_relationship(self, user: User, activity: Activity, organization_role: str):
        """用户是活动的组织者或主办方"""
        with self.driver.session() as session:
            session.write_transaction(self._create_organizes, user, activity, organization_role)

    @staticmethod
    def _create_organizes(tx, user: User, activity: Activity, organization_role: str):
        """创建用户是活动组织者的关系"""
        query = (
            "MATCH (u:User {user_id: $user_id}), (a:Activity {activity_id: $activity_id}) "
            "CREATE (u)-[r:ORGANIZES {organization_role: $organization_role}]->(a)"
        )
        tx.run(query, 
               user_id=user.user_id, 
               activity_id=activity.activity_id, 
               organization_role=organization_role)

    # 创建用户是活动工作人员的关系
    def create_acted_in_relationship(self, user: User, activity: Activity, organization_role: str):
        """用户是活动的工作人员"""
        with self.driver.session() as session:
            session.write_transaction(self._create_acted_in, user, activity, organization_role)

    @staticmethod
    def _create_acted_in(tx, user: User, activity: Activity, organization_role: str):
        """创建用户是活动工作人员的关系"""
        query = (
            "MATCH (u:User {user_id: $user_id}), (a:Activity {activity_id: $activity_id}) "
            "CREATE (u)-[r:ACTED_IN {organization_role: $organization_role}]->(a)"
        )
        tx.run(query, 
               user_id=user.user_id, 
               activity_id=activity.activity_id, 
               organization_role=organization_role)


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
        activity_id="AI Work",
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
    db = Neo4jDatabase(uri="bolt://localhost:7687", username="neo4j", password="szdxwllyk1585")
    
    rating = 4  # 例如，用户给活动评分 4
    comments = "The workshop was very insightful and informative."  # 用户的评论

    # 创建兴趣程度、组织角色等属性
    interest_level = "High"  # 用户对活动的兴趣程度
    organization_role_org = "Organizer"  # 用户在活动中的角色（作为主办方）
    organization_role_act = "Host"  # 用户在活动中的角色（作为工作人员）
    
    # 创建用户节点
    db.create_user_node(user)
    
    # 创建活动节点
    db.create_activity_node(activity)
    
    # 创建用户参与活动的关系，并添加评分和评论
    db.create_participation_relationship(user, activity, rating, comments)

     # 创建用户对活动的兴趣关系
    db.create_interested_in_relationship(user, activity, interest_level)
    
    # 创建用户作为活动主办方的关系
    db.create_organizes_relationship(user, activity, organization_role_org)
    
    # 创建用户作为活动工作人员的关系
    db.create_acted_in_relationship(user, activity, organization_role_act)
    
    db.close()