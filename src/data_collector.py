import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import feedparser

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
    
    def fetch_cointelegraph(self):
        url = "https://cointelegraph.com/rss"
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries:
            summary = entry.get('summary', '')
            articles.append({
                'title': entry.get('title', '').strip(),
                'url': entry.get('link', ''),
                'summary': summary.strip(),
                'source': 'Cointelegraph'
            })
        return articles

    def fetch_newsbtc(self):
        url = "https://www.newsbtc.com/feed/"
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries:
            summary = entry.get('summary', '')
            articles.append({
                'title': entry.get('title', '').strip(),
                'url': entry.get('link', ''),
                'summary': summary.strip(),
                'source': 'NewsBTC'
            })
        return articles

    def fetch_google_news(self, query="crypto"):
        url = f"https://news.google.com/rss/search?q={query}"
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries:
            articles.append({
                'title': entry.get('title', '').strip(),
                'url': entry.get('link', ''),
                'summary': entry.get('summary', '').strip(),
                'source': 'Google News'
            })
        return articles
    
    def fetch_google_finance_prices(self):
        url = "https://www.google.com/finance/markets/cryptocurrencies"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tickers = []
        for li in soup.select('ul.sbnBtf > li'):
            try:
                symbol = li.select_one('div.COaKTb')
                name = li.select_one('div.ZvmM7')
                price = li.select_one('div.YMlKec')
                change = li.select_one('span.P2Luy')
                percent = li.select_one('div.JwB6zf')
                percent_value = float(percent.text.replace('%', '').replace('+', '').replace('−', '-')) if percent else None
                if symbol and name and price:
                    tickers.append({
                        'symbol': symbol.text.strip(),
                        'name': name.text.strip(),
                        'price': float(price.text.replace(',', '').replace('$', '')),
                        'change': float(change.text.replace(',', '').replace('+', '').replace('%', '')) if change else None,
                        'percent_change': percent_value,
                        'price_change_percentage_24h': percent_value,
                        'source': 'Google Finance'
                    })
            except Exception:
                continue
        return tickers

    def fetch_market_data(self):
        # Aggregate from all sources
        all_articles = []
        all_articles.extend(self.fetch_coingecko())
        all_articles.extend(self.fetch_coinmarketcap())
        all_articles.extend(self.fetch_cryptopanic())
        all_articles.extend(self.fetch_coindesk())
        all_articles.extend(self.fetch_cointelegraph())
        all_articles.extend(self.fetch_newsbtc())
        all_articles.extend(self.fetch_google_news())
        # Add Google Finance price data
        google_finance_prices = self.fetch_google_finance_prices()
        all_articles.extend(google_finance_prices)
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