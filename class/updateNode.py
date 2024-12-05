from DataBase import Neo4jDatabase
from User import User
from Activity import Activity
from datetime import datetime

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


    db = Neo4jDatabase(uri="bolt://localhost:7687", username="neo4j", password="kkykkykky")

    # 读取用户节点
    user_data = db.read_user_node(user_id="12345")
    print("User Data:", user_data)

    # 读取活动节点
    activity_data = db.read_activity_node(activity_id="AI Work")
    print("Activity Data:", activity_data)

    # 根据活动标题读取活动节点
    activities_by_title = db.read_nodes_by_property(node_type="Activity", property_name="title",
                                                    value="Test update")
    print("Activities found by title:", activities_by_title)

    db.close()
    print("Operations completed.")