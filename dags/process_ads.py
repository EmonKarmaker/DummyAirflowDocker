import json
from datetime import datetime

def process_ads():
    with open('ads_data.json', 'r', encoding='utf-8') as file:
        ads_data = json.load(file)

    for ad in ads_data:
        ad['_id'] = ad['url'].split('finnkode=')[-1]
        ad['processed_date'] = datetime.now().strftime('%Y-%m-%d')

    # Save processed data
    with open('processed_ads.json', 'w', encoding='utf-8') as file:
        json.dump(ads_data, file, ensure_ascii=False, indent=4)

    print(f"Processed {len(ads_data)} ads.")

if __name__ == "__main__":
    process_ads()
