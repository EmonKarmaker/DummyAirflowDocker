from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['finn_scraper']
collection = db['ads']

# Count documents
print("Total ads in MongoDB:", collection.count_documents({}))

# Example query
ad = collection.find_one({"_id": "example_id"})
print("Example ad:", ad)
