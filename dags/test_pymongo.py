from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
print("Connected to MongoDB:", client.list_database_names())
