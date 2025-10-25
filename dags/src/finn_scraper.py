import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Step 1: Initialize Selenium WebDriver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Automatically manages the ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Step 2: Extract URLs from the main page
def extract_urls(driver):
    url = "https://www.finn.no/realestate/newbuildings/search.html"
    driver.get(url)

    # Wait for the page to load
    driver.implicitly_wait(10)

    # Get page source and parse with BeautifulSoup
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # Locate the script tag containing `window.__remixContext`
    script_tag = soup.find('script', string=lambda t: t and 'window.__remixContext' in t)
    if not script_tag:
        raise ValueError("JSON data not found in the script tag.")

    # Debugging: Print the raw content for verification
    raw_script_content = script_tag.string
    print("Raw Script Content (First 500 chars):", raw_script_content[:500])

    # Extract JSON data
    try:
        # Extract only the JSON part
        json_start = raw_script_content.find('{')
        json_end = raw_script_content.rfind('}') + 1
        json_data = raw_script_content[json_start:json_end]

        # Parse JSON
        data = json.loads(json_data)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        raise

    # Extract main ad data
    main_data = data.get('state', {}).get('loaderData', {}).get(
        'routes/realestate+/_search+/$subvertical.search[.html]', {}
    ).get('results', {}).get('docs', [])
    if not main_data:
        raise ValueError("No ads found in the JSON data.")

    # Extract canonical URLs
    ad_urls = [ad['canonical_url'] for ad in main_data]
    return ad_urls

# Step 3: Extract details from each ad
def scrape_ad_details(driver, ad_url):
    driver.get(ad_url)

    # Wait for the page to load
    driver.implicitly_wait(10)

    # Parse the ad page
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract required data
    heading = soup.find('h1').text if soup.find('h1') else None
    sub_heading = soup.find('h2').text if soup.find('h2') else None

    nøkkelinfo = {}
    nøkkelinfo_section = soup.find('div', class_='key-information-section')
    if nøkkelinfo_section:
        for item in nøkkelinfo_section.find_all('div', class_='key-info-item'):
            key = item.find('span', class_='key-info-title').text.strip()
            value = item.find('span', class_='key-info-value').text.strip()
            nøkkelinfo[key] = value

    matrikkelinformasjon = {}
    matrikkelinformasjon_section = soup.find('div', class_='property-details-section')
    if matrikkelinformasjon_section:
        for item in matrikkelinformasjon_section.find_all('div', class_='property-detail-item'):
            key = item.find('span', class_='property-detail-title').text.strip()
            value = item.find('span', class_='property-detail-value').text.strip()
            matrikkelinformasjon[key] = value

    facilities = []
    facilities_section = soup.find('div', class_='facilities-section')
    if facilities_section:
        facilities = [li.text.strip() for li in facilities_section.find_all('li')]

    # Extract FinnCode and Date
    finn_code = ad_url.split('finnkode=')[-1]
    date = soup.find('time', {'class': 'publish-date'}).text if soup.find('time', {'class': 'publish-date'}) else None

    # Return extracted ad data
    return {
        '_id': finn_code,
        'heading': heading,
        'sub_heading': sub_heading,
        'nøkkelinfo': nøkkelinfo,
        'matrikkelinformasjon': matrikkelinformasjon,
        'facilities': facilities,
        'date': date
    }

# Step 4: Main function to scrape all ads
def scrape_all_ads():
    driver = initialize_driver()

    try:
        # Extract ad URLs
        print("Extracting URLs...")
        ad_urls = extract_urls(driver)

        # Scrape details for each ad
        all_ads = []
        for ad_url in ad_urls:
            print(f"Scraping ad: {ad_url}")
            ad_details = scrape_ad_details(driver, ad_url)
            all_ads.append(ad_details)

        return all_ads

    finally:
        driver.quit()

# Step 5: Run the scraper and save results
if __name__ == "__main__":
    try:
        ads_data = scrape_all_ads()

        # Save data to JSON file
        with open('ads_data.json', 'w', encoding='utf-8') as f:
            json.dump(ads_data, f, ensure_ascii=False, indent=4)

        print("Data scraping completed. Results saved to 'ads_data.json'.")
    except Exception as e:
        print("An error occurred:", e)
