from neo4j import GraphDatabase
import csv

class Database:
    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def create_relationship(self, user_id, activity_id, relationship_type, properties):
        # 构建查询语句
        query = f"""
        MATCH (u:User {{user_id: "{user_id}"}}), (a:Activity {{activity_id: {activity_id}}})
        MERGE (u)-[r:{relationship_type}]->(a)
        SET r += {{ {', '.join([f'{key}: "{value}"' for key, value in properties.items()])} }}
        """
        
        # 执行查询
        with self._driver.session() as session:
            session.run(query)

    def batch_insert_relationships_from_csv(self, csv_file_path):
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 获取 CSV 行中的数据
                user_id = row['user_id']
                activity_id = row['activity_id']
                
                # 创建 PARTICIPATED_IN 关系
                rating = row['rating']
                comments = row['comments']
                self.create_relationship(user_id, activity_id, 'PARTICIPATED_IN', {'rating': rating, 'comments': comments})
                
                # 创建 INTERESTED_IN 关系
                interest_level = row['interest_level']
                self.create_relationship(user_id, activity_id, 'INTERESTED_IN', {'interest_level': interest_level})
                
                # 创建 ORGANIZES 关系
                organization_role = row['organization_role']
                self.create_relationship(user_id, activity_id, 'ORGANIZES', {'role': organization_role})

# 示例使用
db = Database(uri="bolt://localhost:7687", user="neo4j", password="kkykkykky")

# 批量插入 CSV 数据中的关系
db.batch_insert_relationships_from_csv('/home/kky/RecommendSystem/packageClass/Recommend_info/realtion.csv')

# 关闭数据库连接
db.close()
