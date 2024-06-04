
import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    try:
        # Assuming you are using requests and BeautifulSoup for scraping
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        data = soup.get_text()
        print("Scraped data:", data)  # Output scraped data
        return data
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
