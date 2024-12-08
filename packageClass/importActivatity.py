import csv
from neo4j import GraphDatabase

class ActivityDatabase:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def import_activities_from_csv(self, csv_file_path):
        """逐行读取CSV文件并插入活动数据"""
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    self.insert_activity(
                        activity_id=row['activity_id'],
                        name=row['name'],
                        date=row['date'],
                        location=row['location'],
                        tags=eval(row['tags'])  # 将字符串列表转换为实际列表
                    )
                except Exception as e:
                    print(f"插入活动 {row['activity_id']} 失败: {e}")

    def insert_activity(self, activity_id, name, date, location, tags):
        """插入单个活动数据到Neo4j"""
        with self.driver.session() as session:
            session.write_transaction(
                self._insert_activity_transaction,
                activity_id, name, date, location, tags
            )

    @staticmethod
    def _insert_activity_transaction(tx, activity_id, name, date, location, tags):
        query = """
        CREATE (a:Activity {activity_id: $activity_id, name: $name, date: $date, location: $location, tags: $tags})
        """
        tx.run(query, activity_id=activity_id, name=name, date=date, location=location, tags=tags)

# 示例使用
if __name__ == "__main__":
    db = ActivityDatabase("bolt://localhost:7687", "neo4j", "kkykkykky")
    csv_file = "/home/kky/RecommendSystem/packageClass/Recommend_info/activity_info.csv"  # 替换为实际路径

    try:
        db.import_activities_from_csv(csv_file)
        print("活动数据导入完成！")
    except Exception as e:
        print(f"导入活动数据时出错: {e}")
    finally:
        db.close()
