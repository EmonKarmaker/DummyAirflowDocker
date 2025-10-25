from pymongo import MongoClient
import json

# Connect to MongoDB
def connect_to_mongo():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['finn_scraper']
    collection = db['ads']
    return collection

# Check for existing documents
def check_existing_ads(collection, ads_data):
    existing_ids = set(doc['_id'] for doc in collection.find({}, {'_id': 1}))
    new_ads = [ad for ad in ads_data if ad['_id'] not in existing_ids]
    return new_ads

# Insert new ads into MongoDB
def upload_to_mongo(collection, new_ads):
    if new_ads:
        collection.insert_many(new_ads)
        print(f"Uploaded {len(new_ads)} new ads to MongoDB.")
    else:
        print("No new ads to upload.")

# Main function
def main():
    # Load processed ads from JSON
    with open('processed_ads.json', 'r', encoding='utf-8') as file:
        ads_data = json.load(file)

    # Connect to MongoDB
    collection = connect_to_mongo()

    # Filter and upload
    new_ads = check_existing_ads(collection, ads_data)
    print(f"Found {len(new_ads)} new ads to upload.")
    upload_to_mongo(collection, new_ads)

if __name__ == "__main__":
    main()
