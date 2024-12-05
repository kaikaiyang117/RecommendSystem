
from neo4j import GraphDatabase

uri = "bolt://172.31.225.146:7474/"  # Neo4j数据库的URI
username = "neo4j"  # 数据库用户名
password = "kkykkykky"  # 数据库密码

# 创建连接
driver = GraphDatabase.driver(uri, auth=(username, password))