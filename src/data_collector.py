import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

class DataCollector:
    def __init__(self):
        pass
    
    def fetch_coingecko(self):
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
                    'summary': summary.text.strip() if summary else '',
                    'source': 'CoinGecko'
                })
        return articles
    
    def fetch_coinmarketcap(self):
        url = "https://coinmarketcap.com/headlines/news/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        for article in soup.select('a.iuljz6-0.bhXxYA'):  # News article links
            title = article.select_one('h3')
            link = article.get('href')
            if title and link:
                articles.append({
                    'title': title.text.strip(),
                    'url': link if link.startswith('http') else f"https://coinmarketcap.com{link}",
                    'summary': '',
                    'source': 'CoinMarketCap'
                })
        return articles
    
    def fetch_cryptopanic(self):
        url = "https://cryptopanic.com/news/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        for article in soup.select('div.news_item'):
            title = article.select_one('a.news_title')
            link = title.get('href') if title else None
            if title and link:
                articles.append({
                    'title': title.text.strip(),
                    'url': link,
                    'summary': '',
                    'source': 'CryptoPanic'
                })
        return articles
    
    def fetch_coindesk(self):
        url = "https://www.coindesk.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        for article in soup.select('a.card-title-link'):  # Main news links
            title = article.text.strip()
            link = article.get('href')
            if title and link:
                articles.append({
                    'title': title,
                    'url': link if link.startswith('http') else f"https://www.coindesk.com{link}",
                    'summary': '',
                    'source': 'CoinDesk'
                })
        return articles
    
    def fetch_market_data(self):
        # Aggregate from all sources
        all_articles = []
        all_articles.extend(self.fetch_coingecko())
        all_articles.extend(self.fetch_coinmarketcap())
        all_articles.extend(self.fetch_cryptopanic())
        all_articles.extend(self.fetch_coindesk())
        # Save to file
        os.makedirs('data', exist_ok=True)
        with open('data/market-data.json', 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'data': all_articles
            }, f, indent=2)
        return all_articles

if __name__ == "__main__":
    collector = DataCollector()
    collector.fetch_market_data()
    print("Market data collected successfully!") 