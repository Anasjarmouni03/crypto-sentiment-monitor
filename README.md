# Crypto Sentiment Monitor

Multi-source cryptocurrency sentiment analysis platform using web scraping, sentiment analysis, and real-time visualization.

## Project Overview

This project collects cryptocurrency-related content from multiple sources (Reddit, CryptoNews, Cointelegraph), analyzes sentiment using NLP (VADER), and presents insights through an interactive Streamlit dashboard with automated weekly email reports.

**Built by:** Team of 2 developers

**Tech Stack:** Python, BeautifulSoup, SQLite, VADER Sentiment, Streamlit, Plotly

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Anasjarmouni03/crypto-sentiment-monitor.git
cd crypto-sentiment-monitor

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# 1. Collect crypto data
python main_simple.py

# 2. Analyze sentiment
python -c "from analysis.sentiment_analyzer import process_unanalyzed_data; process_unanalyzed_data()"

# 3. Launch interactive dashboard
streamlit run dashboard/app.py

# 4. Send email report (optional)
python -c "from automation.email_reporter import send_weekly_report; send_weekly_report()"
```

---

## Project Architecture

```
crypto-sentiment-monitor/
│
├── scrapers/              # Data Collection Layer
│   └── universal_scraper.py   # Multi-source web scraper
│
├── utils/                 # Core Infrastructure
│   ├── database.py            # SQLite operations
│   └── config.py              # Configuration settings
│
├── analysis/              # Sentiment Analysis Layer
│   ├── sentiment_analyzer.py  # VADER sentiment analysis
│   └── trend_detector.py      # Trend detection algorithms
│
├── dashboard/             # Visualization Layer
│   └── app.py                 # Streamlit dashboard
│
├── automation/            # Automation Layer
│   ├── email_reporter.py      # Email report generation
│   └── scheduler.py           # Task scheduling
│
└── data/                  # Data Storage
    └── crypto_sentiment.db    # SQLite database
```

---

## Features

### Data Collection

- **Multi-source scraping**: Reddit, CryptoNews.io, Cointelegraph
- **Anti-blocking measures**: Rotating user agents, random delays
- **Persistent storage**: SQLite database with full history
- **Real-time collection**: Collects 30-40 posts per run

### Sentiment Analysis

- **VADER sentiment**: Industry-standard sentiment analysis tool
- **Crypto detection**: Identifies 25+ cryptocurrencies mentioned
- **Scoring system**: -1.0 (negative) to +1.0 (positive)
- **Auto-labeling**: Positive, negative, neutral classification

### Visualization

- **Interactive dashboard**: Built with Streamlit
- **Real-time charts**: Sentiment trends over time
- **Trending cryptos**: Most mentioned coins with sentiment breakdown
- **Source comparison**: Compare sentiment across platforms
- **Auto-refresh**: Updates every 5 minutes

### Automation

- **Email reports**: Weekly sentiment summaries
- **Scheduled jobs**: Automatic data collection
- **Configurable timing**: Customizable schedules

---

## Data Sources

| Source        | Type              | Content                           | Engagement Metric |
| ------------- | ----------------- | --------------------------------- | ----------------- |
| Reddit        | Social Media      | r/cryptocurrency, r/CryptoMarkets | Upvotes           |
| CryptoNews.io | News              | Latest crypto articles            | N/A               |
| Cointelegraph | Professional News | Expert analysis                   | N/A               |

**Collection Rate:** Approximately 30-40 items per run  
**Recommended Schedule:** Every 2-3 hours for continuous monitoring

---

## Database Schema

```sql
CREATE TABLE scraped_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,           -- Platform name
    content TEXT NOT NULL,           -- Post/article text
    timestamp DATETIME NOT NULL,     -- Publication time
    url TEXT,                        -- Source URL
    engagement_score INTEGER,        -- Upvotes/likes
    scraped_at DATETIME,            -- Collection time
    sentiment_score REAL,            -- -1.0 to +1.0
    sentiment_label TEXT,            -- positive/negative/neutral
    crypto_mentioned TEXT            -- Detected cryptocurrencies
);
```

---

## Configuration

Edit `utils/config.py` to customize:

```python
# Scraping settings
SCRAPE_LIMIT = 50           # Posts per source
REQUEST_DELAY = 2           # Seconds between requests

# Email settings (for reports)
EMAIL_SENDER = 'your@email.com'
EMAIL_RECIPIENTS = ['recipient@email.com']

# Cryptocurrencies to track
CRYPTO_LIST = ['BTC', 'ETH', 'SOL', 'ADA', ...]  # 25+ supported
```

---

## Performance Metrics

- **Collection Speed:** 30-40 items in 5-10 seconds
- **Analysis Speed:** Processes approximately 100 items per second
- **Dashboard Load Time:** Under 2 seconds with 500+ entries
- **Storage Efficiency:** Approximately 1MB per 1000 entries

---

## Technical Implementation

### ETL Pipeline

1. **Extract**: Web scraping from multiple sources using BeautifulSoup
2. **Transform**: Sentiment analysis using VADER, cryptocurrency detection
3. **Load**: Store processed data in SQLite with sentiment scores

### Key Technologies

- **BeautifulSoup4**: HTML parsing and web scraping
- **VADER Sentiment**: Pre-trained sentiment analysis model
- **SQLite**: Lightweight database for data persistence
- **Streamlit**: Interactive dashboard framework
- **Plotly**: Dynamic data visualization
- **APScheduler**: Background task scheduling

---

## Development Team

- **Data Collection Team**: Web scraping implementation, database design, data pipeline architecture
- **Analysis Team**: Sentiment analysis algorithms, trend detection, dashboard development, automation

---

## Future Enhancements

- Integration with additional data sources (Twitter API, Telegram channels)
- Machine learning models for price prediction correlation
- Real-time WebSocket connections for live updates
- Historical data analysis and pattern recognition
- API endpoint for external integrations

---

## License

This project is an educational project developed for academic purposes.

---

## Acknowledgments

- VADER Sentiment Analysis library by C.J. Hutto
- Streamlit framework for rapid dashboard development
- Data sources: Reddit, CryptoNews.io, Cointelegraph

---

For questions or contributions, please open an issue on GitHub.

## 🏗️ Project Structure

```
crypto-sentiment-monitor/
│
├── data/                           # Database storage
│   └── crypto_sentiment.db         # SQLite database
│
├── utils/                          # Core utilities
│   ├── database.py                 # Database operations
│   └── config.py                   # Configuration settings
│
├── scrapers/                       # Data collection
│   └── universal_scraper.py        # Multi-source web scraper
│
├── analysis/                       # Sentiment analysis (Friend's work)
│   ├── sentiment_analyzer.py       # VADER sentiment analysis
│   └── trend_detector.py           # Trend detection algorithms
│
├── dashboard/                      # Visualization (Friend's work)
│   └── app.py                      # Streamlit dashboard
│
├── automation/                     # Reporting (Friend's work)
│   ├── email_reporter.py           # Email report generation
│   └── scheduler.py                # Task scheduling
│
├── main_simple.py                  # Main scraper orchestrator
└── requirements.txt                # Python dependencies
```

---

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Data Collection

```bash
python main_simple.py
```

This will:

- Initialize the database
- Scrape Reddit, CryptoNews, and Cointelegraph
- Store data in `data/crypto_sentiment.db`
- Display collection summary

### 3. Run Analysis (After friend completes their part)

```bash
# Analyze sentiment
python -c "from analysis.sentiment_analyzer import process_unanalyzed_data; process_unanalyzed_data()"

# Launch dashboard
streamlit run dashboard/app.py

# Send weekly report
python -c "from automation.email_reporter import send_weekly_report; send_weekly_report()"
```

---

## 📊 Data Collection

### Sources

- **Reddit**: r/cryptocurrency, r/CryptoMarkets, r/Bitcoin
- **CryptoNews.io**: Latest crypto news articles
- **Cointelegraph**: Professional crypto journalism

### Database Schema

```sql
CREATE TABLE scraped_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,           -- 'reddit', 'cryptonews', 'cointelegraph'
    content TEXT NOT NULL,           -- Post/article text
    timestamp DATETIME NOT NULL,     -- Publication time
    url TEXT,                        -- Source URL
    engagement_score INTEGER,        -- Upvotes/likes
    scraped_at DATETIME,            -- Collection time
    sentiment_score REAL,            -- -1.0 to +1.0 (added by analysis)
    sentiment_label TEXT,            -- 'positive', 'negative', 'neutral'
    crypto_mentioned TEXT            -- Comma-separated crypto symbols
);
```

### Collection Schedule

Recommended: Run `python main_simple.py` every 2-3 hours to build a rich dataset.

```bash
# Morning
python main_simple.py

# Afternoon
python main_simple.py

# Evening
python main_simple.py
```

---

## 🔧 Technical Details

### Data Collection Features

- **SSL/TLS Handling**: Automatic certificate issue resolution
- **Anti-blocking**: Rotating user agents and random delays
- **Multi-source**: Fallback mechanisms if sources fail
- **Error Handling**: Graceful degradation, continues on failures
- **Deduplication**: Prevents duplicate entries

### Database Functions

```python
from utils.database import (
    init_database,           # Create database tables
    insert_scraped_data,     # Add scraped content
    get_unanalyzed_data,     # Fetch unanalyzed entries
    update_sentiment,        # Update with analysis results
    get_data_by_timerange,   # Query by time period
    get_stats                # Database statistics
)
```

---

## 📈 Expected Results

### Per Collection Run

- Reddit: 25-30 posts
- CryptoNews: 3-5 articles
- Cointelegraph: 1-3 articles
- **Total: ~30-40 items per run**

### After 5 Runs

- ~150-200 total entries
- Rich dataset for sentiment analysis
- Multiple timeframes for trend detection

---

## 🛠️ Troubleshooting

### No data collected?

```bash
# Check internet connection
ping google.com

# Try with fresh install
pip install --upgrade requests beautifulsoup4

# Check database
python -c "from utils.database import get_stats; print(get_stats())"
```

### SSL certificate errors?

The scraper automatically handles this, but if issues persist:

```bash
# Set environment variable
set SSL_CERT_FILE=
set REQUESTS_CA_BUNDLE=

# Then run
python main_simple.py
```

### Reddit blocked?

- Normal! Reddit rate-limits aggressively
- Wait 30-60 minutes between runs
- The scraper tries multiple subreddits automatically

---

## 📦 For Your Teammate

### Files to Share

1. `utils/database.py` - Database interface
2. `utils/config.py` - Shared configuration
3. `data/crypto_sentiment.db` - Collected data (after runs)
4. Requirements document (already provided)

### Integration Points

Your teammate should:

1. Import from `utils.database`
2. Use functions: `get_unanalyzed_data()`, `update_sentiment()`
3. Read config from `utils.config`
4. **Never** modify database schema or scraper code

---

## 🎯 Project Goals

- [x] Multi-source web scraping
- [x] Robust error handling
- [x] SQLite data storage
- [ ] Sentiment analysis (Friend's task)
- [ ] Trend detection (Friend's task)
- [ ] Interactive dashboard (Friend's task)
- [ ] Email automation (Friend's task)

---

## 📝 Notes

- **Data Collection**: Complete and functional
- **Analysis Layer**: Waiting on teammate
- **No API keys required**: All scraping uses public endpoints
- **Ethical scraping**: Respects rate limits, uses delays

---

## 🚀 Future Enhancements

- Add more sources (Twitter API if available, news APIs)
- Implement caching to reduce redundant requests
- Add data export functionality (CSV, JSON)
- Historical data analysis
- Price correlation tracking

---

## 📄 License

Educational project for Python course.

---

**Status**: Data Collection Layer ✅ Complete | Analysis Layer 🔄 In Progress

**Last Updated**: January 3, 2026
