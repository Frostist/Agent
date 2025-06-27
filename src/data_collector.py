import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

class DataCollector:
    def __init__(self):
        pass
    
    def fetch_market_data(self):
        """Scrape latest blog articles from CoinGecko Learn page"""
        url = "https://www.coingecko.com/learn"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        for article in soup.select('a.tw-block.tw-group.tw-relative.tw-w-full.tw-h-full.tw-no-underline'):
            title = article.select_one('h2')
            summary = article.select_one('p')
            link = article.get('href')
            if title and link:
                articles.append({
                    'title': title.text.strip(),
                    'url': f"https://www.coingecko.com{link}",
                    'summary': summary.text.strip() if summary else ''
                })
        # Save to file
        os.makedirs('data', exist_ok=True)
        with open('data/market-data.json', 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'data': articles
            }, f, indent=2)
        return articles

if __name__ == "__main__":
    collector = DataCollector()
    collector.fetch_market_data()
    print("Market data collected successfully!") 