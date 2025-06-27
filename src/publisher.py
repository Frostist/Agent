import os
import requests
import json
from datetime import datetime
import glob

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
        
    def send_message(self, text, parse_mode='Markdown'):
        """Send message to Telegram"""
        if not self.bot_token or not self.chat_id:
            print("Telegram credentials not configured")
            return False
            
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
        """Send market analysis update"""
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