import csv
from neo4j import GraphDatabase

class ActivityDatabase:
    def __init__(self, uri, user, password):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def import_activities_from_csv(self, csv_file_path):
        with self.driver.session() as session:
            session.write_transaction(self._load_csv_and_create_activities, csv_file_path)

    def _load_csv_and_create_activities(self, tx, csv_file_path):
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                activity_id = row['activity_id']
                title = row['title']
                description = row['description']
                sponsor = row['sponsor']
                tags = row['tags']
                date = row['date']
                location = row['location']
                duration = row['duration']
                audience = row['audience']
                capacity = row['capacity']
                current_participants = row['current_participants']
                organizer = row['organizer']
                img_url = row['img_url']
                
                query = (
                    f"CREATE (a:Activity {{activity_id: {activity_id}, title: '{title}', description: '{description}', "
                    f"sponsor: '{sponsor}', tags: {tags}, date: datetime('{date}'), location: '{location}', "
                    f"duration: {duration}, audience: '{audience}', capacity: {capacity}, "
                    f"current_participants: {current_participants}, organizer: '{organizer}', img_url: '{img_url}'}})"
                )
                try:
                    tx.run(query)
                    print(f"Inserted activity {activity_id} successfully.")
                except Exception as e:
                    print(f"Failed to insert activity {activity_id}: {e}")

if __name__ == "__main__":
    db = ActivityDatabase(uri="bolt://localhost:7687", user="neo4j", password="kkykkykky")
    CSV_FILE = "/home/kky/RecommendSystem/packageClass/Recommend_info/activity_info.csv"
    db.import_activities_from_csv(CSV_FILE)
    db.close()
