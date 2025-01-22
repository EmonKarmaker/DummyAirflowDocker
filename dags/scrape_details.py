import requests
from bs4 import BeautifulSoup
import json

def scrape_ad_details():
    with open('ad_links.json', 'r', encoding='utf-8') as file:
        ad_links = json.load(file)

    ads_data = []
    for ad_url in ad_links:
        response = requests.get(ad_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract details
        heading = soup.find('h1').text if soup.find('h1') else None
        sub_heading = soup.find('h2').text if soup.find('h2') else None

        facilities = [li.text.strip() for li in soup.find_all('li', class_='facility')]

        ad_data = {
            "url": ad_url,
            "heading": heading,
            "sub_heading": sub_heading,
            "facilities": facilities,
        }
        ads_data.append(ad_data)

    # Save details to JSON
    with open('ads_data.json', 'w', encoding='utf-8') as file:
        json.dump(ads_data, file, ensure_ascii=False, indent=4)

    print(f"Scraped details for {len(ads_data)} ads.")

if __name__ == "__main__":
    scrape_ad_details()
