import csv
from neo4j import GraphDatabase

class DataBase:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def import_users_from_csv_alternatively(self, csv_file_path):
        """逐行读取 CSV 并导入用户节点"""
        with self.driver.session() as session:
            with open(csv_file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    session.write_transaction(self._create_user_node, row)

    @staticmethod
    def _create_user_node(tx, row):
        """插入单个用户节点"""
        query = """
        MERGE (u:User {user_id: $user_id})
        SET u.name = $name,
            u.email = $email,
            u.major = $major,
            u.college = $college,
            u.tags = split($tags, ','),
            u.participation_count = toInteger($participation_count),
            u.created_at = datetime($created_at),
            u.updated_at = datetime($updated_at)
        """
        tx.run(query, **row)

if __name__ == "__main__":
    db = DataBase(uri="bolt://localhost:7687", user="neo4j", password="kkykkykky")
    db.import_users_from_csv_alternatively("/home/kky/RecommendSystem/packageClass/Recommend_info/user_info.csv")
    db.close()
