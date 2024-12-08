from neo4j import GraphDatabase

class Neo4jDatabase:
    def __init__(self, uri, user, password):
        # 初始化连接到 Neo4j 数据库
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def close(self):
        # 关闭数据库连接
        self._driver.close()

    def query_user_by_id(self, user_id):
        # 根据 user_id 查询用户信息并返回字典格式
        query = """
        MATCH (u:User {user_id: $user_id})
        RETURN u
        """
        with self._driver.session() as session:
            result = session.run(query, user_id=user_id)
            user = result.single()
            if user:
                # 将用户节点的属性转换为字典
                user_dict = dict(user["u"].items())
                return user_dict
            else:
                return None  # 如果没有找到对应的用户

# 使用示例
if __name__ == "__main__":
    # 替换为实际的 Neo4j 数据库 URI、用户名和密码
    db = Neo4jDatabase(uri="bolt://localhost:7687", user="neo4j", password="kkykkykky")
    
    # 查询用户信息并返回字典
    user_dict = db.query_user_by_id("1001")  # 替换为实际的用户 ID
    if user_dict:
        print("用户信息:", user_dict)
    else:
        print("未找到对应的用户")
    
    # 关闭连接
    db.close()
