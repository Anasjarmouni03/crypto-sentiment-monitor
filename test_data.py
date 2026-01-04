"""
Test Data Generator
Creates mock database for testing the Analysis & Presentation Layer
Run this BEFORE testing your modules if you don't have the scraper team's database yet
"""

import sqlite3
from datetime import datetime, timedelta
import os

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Connect to database
conn = sqlite3.connect('data/crypto_sentiment.db')
cursor = conn.cursor()

# Create table with exact schema from requirements
cursor.execute('''CREATE TABLE IF NOT EXISTS scraped_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    url TEXT,
    engagement_score INTEGER DEFAULT 0,
    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    sentiment_score REAL,
    sentiment_label TEXT,
    crypto_mentioned TEXT
)''')

# Clear existing data
cursor.execute('DELETE FROM scraped_data')

# Generate mock data
mock_data = [
    # Positive Bitcoin tweets
    ('nitter', 'Bitcoin breaking $100k! This is huge! 🚀 #BTC', datetime.now() - timedelta(hours=1), 'https://twitter.com/user1/status1', 450),
    ('nitter', 'BTC is the future of finance. Great time to be alive!', datetime.now() - timedelta(hours=2), 'https://twitter.com/user2/status2', 320),
    ('nitter', 'Just bought more Bitcoin. Feeling bullish! 📈', datetime.now() - timedelta(hours=3), 'https://twitter.com/user3/status3', 180),
    
    # Negative Ethereum content
    ('nitter', 'Ethereum network fees are ridiculous right now. Can\'t afford to use it.', datetime.now() - timedelta(hours=4), 'https://twitter.com/user4/status4', 95),
    ('cryptopanic', 'Ethereum merge causing network instability - developers concerned', datetime.now() - timedelta(hours=5), 'https://cryptopanic.com/news/eth-concerns', 230),
    ('nitter', 'ETH disappointing performance this week. Should have sold earlier.', datetime.now() - timedelta(hours=6), 'https://twitter.com/user5/status5', 67),
    
    # Positive Solana news
    ('coindesk', 'Solana TVL reaches all-time high as DeFi ecosystem flourishes', datetime.now() - timedelta(hours=8), 'https://coindesk.com/solana-tvl-ath', 0),
    ('cryptopanic', 'Major institutions showing increased interest in Solana blockchain', datetime.now() - timedelta(hours=10), 'https://cryptopanic.com/news/sol-institutions', 420),
    ('nitter', 'SOL price action looking strong. Breaking key resistance levels! 💪', datetime.now() - timedelta(hours=12), 'https://twitter.com/user6/status6', 290),
    
    # Mixed sentiment on various cryptos
    ('nitter', 'DOGE still holding strong despite market volatility', datetime.now() - timedelta(hours=14), 'https://twitter.com/user7/status7', 156),
    ('cryptopanic', 'Cardano announces new partnership with major tech company', datetime.now() - timedelta(hours=16), 'https://cryptopanic.com/news/ada-partnership', 340),
    ('coindesk', 'XRP legal battle continues, market remains uncertain', datetime.now() - timedelta(hours=18), 'https://coindesk.com/xrp-legal', 0),
    
    # Recent negative general crypto sentiment
    ('nitter', 'Crypto market bleeding red today. Time to panic? 😰', datetime.now() - timedelta(hours=20), 'https://twitter.com/user8/status8', 78),
    ('cryptopanic', 'Bitcoin and Ethereum lead crypto market downturn', datetime.now() - timedelta(hours=22), 'https://cryptopanic.com/news/market-down', 510),
    ('coindesk', 'Regulatory concerns weigh on cryptocurrency prices globally', datetime.now() - timedelta(hours=24), 'https://coindesk.com/regulation', 0),
    
    # Older positive content (25-48 hours ago)
    ('nitter', 'Bitcoin adoption growing rapidly in developing countries 🌍', datetime.now() - timedelta(hours=26), 'https://twitter.com/user9/status9', 445),
    ('cryptopanic', 'Ethereum developers announce successful testnet upgrade', datetime.now() - timedelta(hours=30), 'https://cryptopanic.com/news/eth-upgrade', 380),
    ('coindesk', 'Polygon (MATIC) sees surge in developer activity', datetime.now() - timedelta(hours=34), 'https://coindesk.com/polygon-devs', 0),
    ('nitter', 'Just staked my AVAX. Feeling confident about Avalanche future! ❄️', datetime.now() - timedelta(hours=38), 'https://twitter.com/user10/status10', 167),
    ('nitter', 'Chainlink oracles powering the next generation of DeFi 🔗', datetime.now() - timedelta(hours=42), 'https://twitter.com/user11/status11', 201),
    
    # Very recent unanalyzed content (0-30 minutes ago)
    ('nitter', 'Breaking: Bitcoin ETF approval rumors circulating! 🚀🚀🚀', datetime.now() - timedelta(minutes=5), 'https://twitter.com/user12/status12', 823),
    ('cryptopanic', 'Major crypto exchange reports record trading volumes', datetime.now() - timedelta(minutes=15), 'https://cryptopanic.com/news/volume-record', 612),
    ('nitter', 'DOGE community raising funds for charitable cause. Love this space! ❤️', datetime.now() - timedelta(minutes=25), 'https://twitter.com/user13/status13', 334),
    
    # Mixed recent content
    ('coindesk', 'Federal Reserve comments on digital currency future', datetime.now() - timedelta(hours=2), 'https://coindesk.com/fed-comments', 0),
    ('nitter', 'BTC and ETH both showing bullish patterns on the charts 📊', datetime.now() - timedelta(hours=3), 'https://twitter.com/user14/status14', 289),
    ('cryptopanic', 'NFT market shows signs of recovery, led by Ethereum projects', datetime.now() - timedelta(hours=4), 'https://cryptopanic.com/news/nft-recovery', 456),
]

# Insert mock data
cursor.executemany('''INSERT INTO scraped_data 
    (source, content, timestamp, url, engagement_score)
    VALUES (?, ?, ?, ?, ?)''', mock_data)

conn.commit()

# Print statistics
cursor.execute('SELECT COUNT(*) FROM scraped_data')
total = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM scraped_data WHERE sentiment_score IS NULL')
unanalyzed = cursor.fetchone()[0]

print("=" * 60)
print("✅ Mock Database Created Successfully!")
print("=" * 60)
print(f"Location: data/crypto_sentiment.db")
print(f"Total entries: {total}")
print(f"Unanalyzed entries: {unanalyzed}")
print(f"Analyzed entries: {total - unanalyzed}")
print()
print("Sources breakdown:")
for source in ['nitter', 'cryptopanic', 'coindesk']:
    cursor.execute('SELECT COUNT(*) FROM scraped_data WHERE source = ?', (source,))
    count = cursor.fetchone()[0]
    print(f"  • {source}: {count} entries")
print()
print("Next steps:")
print("1. Test sentiment analyzer: python analysis/sentiment_analyzer.py")
print("2. Test trend detector: python analysis/trend_detector.py")
print("3. Launch dashboard: streamlit run dashboard/app.py")
print("4. Test email: python automation/email_reporter.py")
print("=" * 60)

conn.close()