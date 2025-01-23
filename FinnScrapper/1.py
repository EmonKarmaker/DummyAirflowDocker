import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Step 1: Initialize Selenium WebDriver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Step 2: Update Ad Details
def update_ad_details(driver, ad):
    ad_url = f"https://www.finn.no/realestate/{ad['_id']}"  # Construct URL
    driver.get(ad_url)

    # Wait for the page to load
    driver.implicitly_wait(10)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # Update nøkkelinfo
    nøkkelinfo_section = soup.find('div', class_='key-information-section')
    if nøkkelinfo_section:
        ad['nøkkelinfo'] = {
            item.find('span', class_='key-info-title').text.strip(): item.find('span', class_='key-info-value').text.strip()
            for item in nøkkelinfo_section.find_all('div', class_='key-info-item')
        }

    # Update matrikkelinformasjon
    matrikkel_section = soup.find('div', class_='property-details-section')
    if matrikkel_section:
        ad['matrikkelinformasjon'] = {
            item.find('span', class_='property-detail-title').text.strip(): item.find('span', class_='property-detail-value').text.strip()
            for item in matrikkel_section.find_all('div', class_='property-detail-item')
        }

    # Update facilities
    facilities_section = soup.find('div', class_='facilities-section')
    if facilities_section:
        ad['facilities'] = [li.text.strip() for li in facilities_section.find_all('li')]

    # Update date
    publish_date = soup.find('time', {'class': 'publish-date'})
    ad['date'] = publish_date.text if publish_date else None

    return ad

# Step 3: Update All Ads
def update_all_ads(ads_data):
    driver = initialize_driver()

    try:
        # Update each ad in the list
        for ad in ads_data:
            print(f"Updating details for ad ID: {ad['_id']}")
            ad = update_ad_details(driver, ad)

    finally:
        driver.quit()

    return ads_data

# Step 4: Main Execution
if __name__ == "__main__":
    try:
        # Load the data from the JSON file
        with open('ads_data.json', 'r', encoding='utf-8') as file:
            ads_data = json.load(file)

        # Update all ads
        updated_ads_data = update_all_ads(ads_data)

        # Save the updated data to a new JSON file
        with open('processed_ads.json', 'w', encoding='utf-8') as file:
            json.dump(updated_ads_data, file, ensure_ascii=False, indent=4)

        print("Updated data saved to 'processed_ads.json'.")

    except Exception as e:
        print("An error occurred:", e)
