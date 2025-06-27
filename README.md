# Crypto AI Agent

This project is an automated crypto market analysis agent that runs on GitHub Actions. It fetches market data, generates analysis and reports using AI, and publishes updates to your repository and Telegram.

## Features
- Automated market analysis every 15 minutes
- Daily comprehensive crypto reports
- Breaking news analysis
- Publishes content to your repo and Telegram
- Runs entirely on GitHub Actions (no server needed)

## Project Structure
```
.github/workflows/         # GitHub Actions workflows
src/                       # Python source code
content/                   # Generated content (reports, analysis)
data/                      # Market data storage
requirements.txt           # Python dependencies
README.md                  # Project documentation
```

## Setup Instructions

1. **Clone this repository**
2. **Create the required directories and files** (see structure above)
3. **Add your API keys** as GitHub Secrets:
   - `GOOGLE_API_KEY` (Gemini)
   - `COINGECKO_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
4. **Push your code** to GitHub
5. **Workflows will run automatically** based on schedule

## Usage
- Market analysis is generated every 15 minutes
- Daily report is generated at 9 AM UTC
- Breaking news can be triggered via webhook
- All content is committed to the repo and optionally sent to Telegram

## Requirements
See `requirements.txt` for Python dependencies.

## Cost
- **GitHub Actions:** Free (within usage limits)

## License
MIT 