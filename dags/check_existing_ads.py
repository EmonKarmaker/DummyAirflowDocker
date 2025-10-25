from pymongo import MongoClient
import json

def check_existing_ads():
    client = MongoClient('mongodb://localhost:27017/')
    collection = client['finn_scraper']['ads']

    with open('processed_ads.json', 'r', encoding='utf-8') as file:
        ads_data = json.load(file)

    existing_ids = set(doc['_id'] for doc in collection.find({}, {'_id': 1}))
    new_ads = [ad for ad in ads_data if ad['_id'] not in existing_ids]

    with open('new_ads.json', 'w', encoding='utf-8') as file:
        json.dump(new_ads, file, ensure_ascii=False, indent=4)

    print(f"Filtered {len(new_ads)} new ads.")

if __name__ == "__main__":
    check_existing_ads()
