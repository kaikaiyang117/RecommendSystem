from neo4j import GraphDatabase
from User import User
from Activity import Activity
from datetime import datetime
from typing import List
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

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

    # 更新User节点的属性
    def update_user_node(self, user_id: str, updated_properties: dict):
        """更新用户节点的属性"""
        with self.driver.session() as session:
            session.write_transaction(self._update_user, user_id, updated_properties)

    @staticmethod
    def _update_user(tx, user_id: str, updated_properties: dict):
        """更新用户节点属性的Cypher查询"""

        # 构造SET子句
        set_clause = ", ".join([f"u.{key} = ${key}" for key in updated_properties])

        # 查询：根据user_id更新属性
        query = f"""
            MATCH (u:User {{user_id: $user_id}})
            SET {set_clause}
        """

        # 执行查询时传递所有的参数
        params = {"user_id": user_id, **updated_properties}
        tx.run(query, **params)

    # 更新Activity节点的属性
    def update_activity_node(self, activity_id: str, updated_properties: dict):
        """更新活动节点的属性"""
        with self.driver.session() as session:
            session.write_transaction(self._update_activity, activity_id, updated_properties)

    @staticmethod
    def _update_activity(tx, activity_id: str, updated_properties: dict):
        """更新活动节点属性的Cypher查询"""

        # 构造SET子句
        set_clause = ", ".join([f"a.{key} = ${key}" for key in updated_properties])

        # 查询：根据activity_id更新属性
        query = f"""
            MATCH (a:Activity {{activity_id: $activity_id}})
            SET {set_clause}
        """

        # 执行查询时传递所有的参数
        params = {"activity_id": activity_id, **updated_properties}
        tx.run(query, **params)

    # 更新用户与活动之间的关系属性
    def update_relationship_property(self, user_id: str, activity_id: str, relationship_type: str,
                                     updated_property: dict):
        """更新用户与活动之间的关系属性"""
        with self.driver.session() as session:
            session.write_transaction(self._update_relationship_property, user_id, activity_id, relationship_type,
                                      updated_property)

    @staticmethod
    def _update_relationship_property(tx, user_id: str, activity_id: str, relationship_type: str,
                                      updated_property: dict):
        """更新用户与活动之间关系的属性"""

        # 构造SET子句
        set_clause = ", ".join([f"r.{key} = ${key}" for key in updated_property])

        # 查询：根据user_id和activity_id更新关系属性
        query = f"""
            MATCH (u:User {{user_id: $user_id}})-[r:{relationship_type}]->(a:Activity {{activity_id: $activity_id}})
            SET {set_clause}
        """

        # 执行查询时传递所有的参数
        params = {"user_id": user_id, "activity_id": activity_id, **updated_property}
        tx.run(query, **params)

if __name__ == "__main__":
    db = Neo4jDatabase(uri="bolt://localhost:7687", username="neo4j", password="kkykkykky")

    # 更新用户节点
    updated_user_properties = {
        "email": "alice_updated@example.com",  # 更新用户邮箱
        "name": "Hude"  # 更新用户名
    }
    db.update_user_node(user_id="12345", updated_properties=updated_user_properties)

    # 更新活动节点
    updated_activity_properties = {
        "title": "Test update",  # 更新活动标题
        "location": "Room 101, Main Building"  # 更新活动地点
    }
    db.update_activity_node(activity_id="AI Work", updated_properties=updated_activity_properties)

    # 更新用户与活动的参与关系属性
    updated_relationship_properties = {
        "rating": 4,  # 更新评分
        "comments": "Very informative session!"  # 更新评论
    }
    db.update_relationship_property(user_id="12345", activity_id="AI Work", relationship_type="PARTICIPATED_IN",
                                    updated_property=updated_relationship_properties)

    db.close()
    print("Activity node and relationship properties updated successfully.")