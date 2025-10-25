from pymongo import MongoClient
import json

def upload_to_mongo():
    client = MongoClient('mongodb://localhost:27017/')
    collection = client['finn_scraper']['ads']

    with open('new_ads.json', 'r', encoding='utf-8') as file:
        new_ads = json.load(file)

    if new_ads:
        collection.insert_many(new_ads)
        print(f"Uploaded {len(new_ads)} new ads to MongoDB.")
    else:
        print("No new ads to upload.")

if __name__ == "__main__":
    upload_to_mongo()
