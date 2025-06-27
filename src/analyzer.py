import os
import json
import google.generativeai as genai
import requests

class ContentGenerator:
    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    
    def load_market_data(self):
        """Load the latest market data"""
        with open('data/market-data.json', 'r') as f:
            return json.load(f)
    
    def analyze_data(self, data):
        """Analyze market data using Gemini model"""
        prompt = "Analyze the following market data and provide insights: " + str(data)
        response = genai.generate_text(prompt=prompt, model="gemini-2.0-flash-exp")
        return response.result

class TelegramNotifier:
    def __init__(self):
        self.api_url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    def send_message(self, message):
        """Send a message via Telegram"""
        data = {
            "chat_id": self.chat_id,
            "text": message
        }
        response = requests.post(self.api_url, json=data)
        if response.status_code == 200:
            print("Notification sent successfully.")
        else:
            print(f"Failed to send notification. Status code: {response.status_code}")

def main():
    print("Starting market analysis...")
    
    # Initialize components
    generator = ContentGenerator()
    notifier = TelegramNotifier()
    
    # Load market data
    market_data = generator.load_market_data()
    
    # Analyze data
    insights = generator.analyze_data(market_data)
    
    # Send insights via Telegram
    notifier.send_message(insights)

if __name__ == "__main__":
    main()