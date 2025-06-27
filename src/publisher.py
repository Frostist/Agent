import os
import requests
import json
from datetime import datetime
import glob
import re
import difflib

class TelegramPublisher:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
    def get_latest_content(self, content_type='market-analysis'):
        """Get the most recent generated content"""
        try:
            pattern = f"content/{content_type}/*.md"
            files = glob.glob(pattern)
            if not files:
                return "No content available"
                
            # Get the most recent file
            latest_file = max(files, key=os.path.getctime)
            
            with open(latest_file, 'r') as f:
                content = f.read()
            
            # Clean up markdown for Telegram
            content = content.replace('**', '*')  # Telegram uses single asterisks
            content = content.replace('###', '*')  # Convert headers
            content = content.replace('##', '*')
            content = content.replace('#', '*')
            
            return content[:4000]  # Telegram message limit
            
        except Exception as e:
            return f"Error getting content: {e}"
        
    def get_two_latest_contents(self, content_type='market-analysis'):
        """Get the two most recent generated contents (excluding headers)"""
        pattern = f"content/{content_type}/*.md"
        files = sorted(glob.glob(pattern), key=os.path.getctime, reverse=True)
        if len(files) < 2:
            return None, None
        def extract_main_content(filepath):
            with open(filepath, 'r') as f:
                lines = f.readlines()
            # Remove header (first two lines)
            return ''.join(lines[2:]).strip()
        latest_content = extract_main_content(files[0])
        prev_content = extract_main_content(files[1])
        return latest_content, prev_content
        
    def is_meaningful_update(self, latest, previous):
        """Return True if the latest content is meaningfully different from the previous one."""
        if not previous:
            return True  # Always send if no previous
        # Consider as 'not meaningful' if the content is nearly identical (ignoring whitespace)
        ratio = difflib.SequenceMatcher(None, latest, previous).ratio()
        if ratio > 0.97:
            return False
        # If both are generic 'no data' messages, don't send
        no_data_phrases = [
            "No price change data available for top movers",
            "no top movers to report",
            "no data on Top Movers",
            "no standout movers in the last 24 hours"
        ]
        if any(phrase.lower() in latest.lower() for phrase in no_data_phrases) and \
           any(phrase.lower() in previous.lower() for phrase in no_data_phrases):
            return False
        return True
        
    def send_message(self, text, parse_mode='MarkdownV2'):
        """Send message to Telegram"""
        if not self.bot_token or not self.chat_id:
            print("Telegram credentials not configured")
            return False
            
        # Escape text for MarkdownV2
        if parse_mode == 'MarkdownV2':
            text = escape_markdown_v2(text)

        url = f"{self.base_url}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_web_page_preview': True
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("✅ Message sent to Telegram successfully")
                return True
            else:
                print(f"❌ Error sending to Telegram: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Exception sending to Telegram: {e}")
            return False
            
    def send_market_update(self):
        """Send market analysis update only if it's meaningfully different from the previous one."""
        latest, previous = self.get_two_latest_contents('market-analysis')
        if not latest:
            print("No latest market analysis content found.")
            return False
        if not self.is_meaningful_update(latest, previous):
            print("No meaningful update in market analysis. Skipping send.")
            return False
        # Reconstruct message for Telegram
        content = self.get_latest_content('market-analysis')
        message = f"🤖 *Crypto Market Update*\n\n{content}"
        return self.send_message(message)
        
    def send_daily_report(self):
        """Send daily report"""
        content = self.get_latest_content('daily-reports')
        
        message = f"📊 *Daily Crypto Report*\n\n{content}"
        return self.send_message(message)
        
    def send_breaking_news(self):
        """Send breaking news analysis"""
        content = self.get_latest_content('breaking-news')
        
        message = f"🚨 *BREAKING CRYPTO NEWS*\n\n{content}"
        return self.send_message(message)
        
    def send_technical_analysis(self):
        """Send technical analysis"""
        content = self.get_latest_content('technical-analysis')
        
        message = f"📈 *Technical Analysis*\n\n{content}"
        return self.send_message(message)

def escape_markdown_v2(text):
    # Escape all special characters for MarkdownV2
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--platforms', default='telegram')
    parser.add_argument('--urgent', action='store_true')
    parser.add_argument('--type', default='market-analysis', 
                       choices=['market-analysis', 'daily-reports', 'breaking-news', 'technical-analysis'])
    args = parser.parse_args()
    
    if 'telegram' in args.platforms:
        publisher = TelegramPublisher()
        
        if args.urgent:
            success = publisher.send_breaking_news()
        elif args.type == 'daily-reports':
            success = publisher.send_daily_report()
        elif args.type == 'technical-analysis':
            success = publisher.send_technical_analysis()
        else:
            success = publisher.send_market_update()
            
        if success:
            print("✅ Telegram notification sent successfully!")
        else:
            print("❌ Failed to send Telegram notification") 