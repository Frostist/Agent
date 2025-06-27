import os
import json
import google.generativeai as genai
from datetime import datetime
import argparse

class ContentGenerator:
    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def load_market_data(self):
        """Load the latest market data"""
        with open('data/market-data.json', 'r') as f:
            return json.load(f)
            
    def generate_quick_analysis(self, market_data):
        """Generate a quick market analysis"""
        top_movers = sorted(
            [x for x in market_data['data'] if 'price_change_percentage_24h' in x],
            key=lambda x: abs(x['price_change_percentage_24h']),
            reverse=True
        )[:5]
        
        if not top_movers:
            return "No price change data available for top movers. Please ensure your data includes 'price_change_percentage_24h'."
        
        prompt = f"""
        You are a professional crypto market analyst.

        Given the following market data (top movers, price changes, volume, and news):

        {json.dumps(top_movers, indent=2)}

        Write a concise, actionable market analysis (max 250 words) that includes:
        - 1-2 sentence summary of overall market sentiment (bullish, bearish, neutral, and why)
        - The top 2-3 coins with the biggest moves: explain possible reasons (news, volume, sector trends)
        - Any notable sector trends (DeFi, Layer 2, meme coins, etc.)
        - Key technical levels (support/resistance) for Bitcoin and Ethereum if data is available
        - 1-2 actionable insights or things for traders to watch today (e.g., "Watch for BTC to break $30k", "DeFi coins showing strength", "Regulatory news impacting sentiment")
        - Use clear markdown formatting and relevant emojis for readability

        If data is missing, state what is missing and provide a general market outlook.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            return f"Market analysis unavailable due to API error: {e}"
        
    def generate_daily_report(self, market_data):
        """Generate comprehensive daily report"""
        prompt = f"""
        Create a comprehensive daily crypto market report based on this data:
        
        {json.dumps(market_data['data'][:10], indent=2)}
        
        Include:
        1. Market overview and total market cap
        2. Top performers and worst performers  
        3. Technical analysis insights
        4. Key support/resistance levels
        5. Market outlook for tomorrow
        6. Risk assessment and trading considerations
        
        Make it professional and informative, around 800-1000 words.
        Format with proper markdown headers and bullet points.
        Include relevant emojis for better readability.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating daily report: {e}")
            return f"Daily report unavailable due to API error: {e}"
            
    def generate_breaking_news_analysis(self, news_content, market_data):
        """Generate analysis for breaking news"""
        prompt = f"""
        BREAKING NEWS ANALYSIS:
        
        News Content: {news_content}
        
        Current Market Data (Top 5 coins):
        {json.dumps(market_data['data'][:5], indent=2)}
        
        Provide immediate analysis covering:
        1. 🚨 What happened (summary)
        2. 📊 Immediate market impact
        3. 🔍 Which cryptocurrencies are most affected
        4. ⏰ Short-term price predictions (next 24-48 hours)
        5. 💡 Trading opportunities and risks
        6. 🎯 Key levels to watch
        
        Keep it urgent, actionable, and under 300 words.
        Use emojis and clear formatting for social media sharing.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating breaking news analysis: {e}")
            return f"Breaking news analysis unavailable: {e}"
        
    def save_content(self, content, content_type):
        """Save generated content to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"content/{content_type}/{timestamp}.md"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            f.write(f"# Crypto Market {content_type.title()}\n")
            f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*\n\n")
            f.write(content)
            
        print(f"Content saved to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=['quick-analysis', 'daily-report'], 
                       default='quick-analysis')
    args = parser.parse_args()
    
    generator = ContentGenerator()
    market_data = generator.load_market_data()
    
    if args.type == 'quick-analysis':
        content = generator.generate_quick_analysis(market_data)
        generator.save_content(content, 'market-analysis')
    elif args.type == 'daily-report':
        content = generator.generate_daily_report(market_data)
        generator.save_content(content, 'daily-reports') 