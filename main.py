
from scraper.scraper import scrape_url
from vector_db.db_manager import insert_vector, text_to_vector

def main():
    urls = [
        'https://u.ae/en/information-and-services#/',
        'https://u.ae/en/information-and-services/visa-and-emirates-id',
        'https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas',
        'https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas/golden-visa'
    ]
    
    for url in urls:
        print(f"Scraping URL: {url}")
        content = scrape_url(url)
        if content:
            vector = text_to_vector(content)
            insert_vector(url, vector)
            print(f"Data inserted for URL: {url}")
        else:
            print(f"No content scraped from {url}")

if __name__ == '__main__':
    main()
