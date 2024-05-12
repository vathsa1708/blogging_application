from pymongo import MongoClient

class Database:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

# MongoDB URI and database name
MONGODB_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "blog_application_db"

# Initialize the database
db = Database(MONGODB_URI, DATABASE_NAME)
