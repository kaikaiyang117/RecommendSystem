from ..packageClass.Activity import Neo4jDatabase
from ..packageClass.Activity import User
from ..packageClass.Activity import Activity
from datetime import datetime


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
    db = Neo4jDatabase(uri="bolt://localhost:7687", username="neo4j", password="kkykkykky")

    rating = 4  # 例如，用户给活动评分 4
    comments = "The workshop was very insightful and informative."  # 用户的评论

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