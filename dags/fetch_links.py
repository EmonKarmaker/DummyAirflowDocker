from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json

def fetch_ad_links():
    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load the page
        url = "https://www.finn.no/realestate/newbuildings/search.html"
        driver.get(url)

        # Get the rendered HTML content
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract script tag with JSON data
        script_tag = soup.find('script', string=lambda t: t and 'window.__remixContext' in t)
        if not script_tag:
            raise ValueError("JSON data not found in the script tag.")

        # Extract JSON data
        raw_script = script_tag.string.split("=", 1)[1].strip(" ;")
        data = json.loads(raw_script)

        # Extract ad links
        ads = data['state']['loaderData']['routes/realestate+/_search+/$subvertical.search[.html]']['results']['docs']
        ad_links = [ad['canonical_url'] for ad in ads]

        # Save links to JSON
        with open('ad_links.json', 'w', encoding='utf-8') as file:
            json.dump(ad_links, file, ensure_ascii=False, indent=4)

        print(f"Fetched {len(ad_links)} ad links.")
    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_ad_links()
