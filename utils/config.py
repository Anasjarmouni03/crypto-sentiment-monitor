"""
Configuration file for Crypto Sentiment Monitor
Shared settings across all modules
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# SCRAPING CONFIGURATION
# ============================================

# Keywords to search for
SCRAPE_KEYWORDS = ['bitcoin', 'ethereum', 'crypto', 'btc', 'eth', 'cryptocurrency']

# How many posts to scrape per source per run
SCRAPE_LIMIT = 50

# Delay between requests (seconds) - be polite to servers!
REQUEST_DELAY = 2

# User-Agent for web scraping
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# SSL Verification - Set to False to bypass certificate issues
# This is safe for web scraping but DON'T use in production apps
VERIFY_SSL = False


# ============================================
# CRYPTOCURRENCY DETECTION LIST
# ============================================

# List of cryptocurrencies to detect in content
# Format: Both ticker symbols and full names
CRYPTO_LIST = [
    # Major cryptos
    'BTC', 'Bitcoin',
    'ETH', 'Ethereum',
    'USDT', 'Tether',
    'BNB', 'Binance Coin',
    'SOL', 'Solana',
    'XRP', 'Ripple',
    'USDC', 'USD Coin',
    'ADA', 'Cardano',
    'DOGE', 'Dogecoin',
    'TRX', 'Tron',
    
    # Other popular cryptos
    'AVAX', 'Avalanche',
    'DOT', 'Polkadot',
    'MATIC', 'Polygon',
    'LINK', 'Chainlink',
    'UNI', 'Uniswap',
    'ATOM', 'Cosmos',
    'LTC', 'Litecoin',
    'BCH', 'Bitcoin Cash',
    'XLM', 'Stellar',
    'ALGO', 'Algorand',
    'VET', 'VeChain',
    'ICP', 'Internet Computer',
    'FIL', 'Filecoin',
    'APT', 'Aptos',
    'ARB', 'Arbitrum',
    'OP', 'Optimism',
]

# Mapping of full names to ticker symbols
CRYPTO_MAPPING = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'tether': 'USDT',
    'binance coin': 'BNB',
    'solana': 'SOL',
    'ripple': 'XRP',
    'usd coin': 'USDC',
    'cardano': 'ADA',
    'dogecoin': 'DOGE',
    'tron': 'TRX',
    'avalanche': 'AVAX',
    'polkadot': 'DOT',
    'polygon': 'MATIC',
    'chainlink': 'LINK',
    'uniswap': 'UNI',
    'cosmos': 'ATOM',
    'litecoin': 'LTC',
    'bitcoin cash': 'BCH',
    'stellar': 'XLM',
}

# List of Nitter instances (Twitter frontends)
NITTER_INSTANCES = [
    'nitter.nl',
    'nitter.mint.lgbt',
    'nitter.pwhl.xyz',
    'nitter.1d4.us',
    'nitter.unixfox.eu',
    'nitter.fdn.fr',
    'nitter.kavin.rocks',
]


# ============================================
# SOURCE URLS
# ============================================

# CryptoPanic - Crypto news aggregator
CRYPTOPANIC_URL = 'https://cryptopanic.com/news/'

# CoinDesk - Professional crypto news
COINDESK_URL = 'https://www.coindesk.com/'
COINDESK_MARKETS_URL = 'https://www.coindesk.com/tag/markets/'


# ============================================
# SENTIMENT ANALYSIS SETTINGS
# ============================================

# Sentiment thresholds
SENTIMENT_POSITIVE_THRESHOLD = 0.05
SENTIMENT_NEGATIVE_THRESHOLD = -0.05

# Labels
SENTIMENT_LABELS = {
    'positive': 'positive',
    'negative': 'negative',
    'neutral': 'neutral'
}


# ============================================
# DISPLAY SETTINGS
# ============================================

# Number of top cryptos to show in reports
TOP_CRYPTOS_COUNT = 10

# Number of recent posts to display
RECENT_POSTS_LIMIT = 20

# Dashboard refresh interval (seconds)
DASHBOARD_REFRESH_INTERVAL = 300  # 5 minutes


# ============================================
# EMAIL CONFIGURATION (BREVO SMTP)
# ============================================

EMAIL_CONFIG = {
    'smtp_server': 'smtp-relay.brevo.com',
    'smtp_port': 587,
    'smtp_username': '9c2474001@smtp-brevo.com',  # Brevo SMTP Login
    'sender_email': 'ayman.janati@cyphx.dev',   # Your verified "From" email address
    'sender_password': os.getenv('SMTP_PASSWORD'),
    'recipients': ['aymanjanatipro@gmail.com', 'aymanjanati08@gmail.com'],
}