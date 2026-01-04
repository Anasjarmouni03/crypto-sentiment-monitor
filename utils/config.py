"""Configuration for crypto sentiment monitor"""

# Cryptocurrency Detection List
CRYPTO_LIST = [
    'BTC', 'Bitcoin',
    'ETH', 'Ethereum',
    'SOL', 'Solana',
    'ADA', 'Cardano',
    'XRP', 'Ripple',
    'DOGE', 'Dogecoin',
    'MATIC', 'Polygon',
    'DOT', 'Polkadot',
    'AVAX', 'Avalanche',
    'LINK', 'Chainlink'
]

# Database Path
DB_PATH = 'data/crypto_sentiment.db'

# Email Configuration (UPDATE THESE!)
EMAIL_SENDER = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_app_password'
EMAIL_RECIPIENTS = ['recipient@email.com']

# Scraping settings (for scraper team)
SCRAPE_KEYWORDS = ['bitcoin', 'ethereum', 'crypto', 'btc', 'eth']
SCRAPE_LIMIT = 50
REQUEST_DELAY = 2