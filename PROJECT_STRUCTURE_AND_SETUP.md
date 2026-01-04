# Crypto Sentiment Monitor - Setup & Testing Guide

## 📁 Project Structure

Create this exact folder structure:

```
crypto-sentiment-monitor/
│
├── data/                          # Auto-created by database
│   └── crypto_sentiment.db        # SQLite database (auto-generated)
│
├── utils/                         # ✅ YOUR CODE
│   ├── __init__.py               # Empty file
│   ├── database.py               # ✅ DONE
│   └── config.py                 # ✅ DONE
│
├── scrapers/                      # ✅ YOUR CODE
│   ├── __init__.py               # Empty file
│   ├── nitter_scraper.py         # ✅ DONE
│   ├── cryptopanic_scraper.py    # ✅ DONE
│   └── coindesk_scraper.py       # ✅ DONE
│
├── analysis/                      # 👥 YOUR FRIEND'S CODE
│   ├── __init__.py               # Empty file
│   ├── sentiment_analyzer.py    # 👥 Friend builds this
│   └── trend_detector.py         # 👥 Friend builds this
│
├── dashboard/                     # 👥 YOUR FRIEND'S CODE
│   ├── __init__.py               # Empty file
│   └── app.py                    # 👥 Friend builds this
│
├── automation/                    # 👥 YOUR FRIEND'S CODE
│   ├── __init__.py               # Empty file
│   ├── email_reporter.py         # 👥 Friend builds this
│   └── scheduler.py              # 👥 Friend builds this
│
├── main.py                        # ✅ DONE - Main orchestrator
├── requirements.txt               # ✅ DONE
└── README.md                      # Optional
```

## 🚀 Setup Instructions

### Step 1: Create Project Folder

```bash
mkdir crypto-sentiment-monitor
cd crypto-sentiment-monitor
```

### Step 2: Create Folder Structure

```bash
# Create all directories
mkdir utils scrapers analysis dashboard automation data

# Create __init__.py files (empty files to make Python recognize folders as packages)
touch utils/__init__.py
touch scrapers/__init__.py
touch analysis/__init__.py
touch dashboard/__init__.py
touch automation/__init__.py
```

### Step 3: Copy Your Code Files

Copy these files I created into their respective folders:

- `utils/database.py`
- `utils/config.py`
- `scrapers/nitter_scraper.py`
- `scrapers/cryptopanic_scraper.py`
- `scrapers/coindesk_scraper.py`
- `main.py`
- `requirements.txt`

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

If you get permission errors, use:

```bash
pip install --user -r requirements.txt
```

Or create a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## 🧪 Testing Your Code (Before Friend's Part)

### Test 1: Database Module

```bash
python utils/database.py
```

**Expected output:**

```
✅ Database initialized successfully!

📊 Database Stats:
Total entries: 0
Analyzed: 0
Unanalyzed: 0
By source: {}
```

**What this does:** Creates `data/crypto_sentiment.db` file

---

### Test 2: Individual Scrapers

**Test Nitter:**

```bash
python scrapers/nitter_scraper.py
```

**Expected output:**

```
🚀 Testing Nitter Scraper...
✅ Found working Nitter instance: nitter.poast.org
🔍 Scraping Nitter: https://nitter.poast.org/search?q=...
📊 Found X tweets
✅ Successfully scraped X tweets from Nitter

📊 Results: X tweets

📝 Sample tweet:
Content: Bitcoin is breaking $100k...
Timestamp: 2024-12-30 14:30:00
Engagement: 450
URL: https://...
```

**Test CryptoPanic:**

```bash
python scrapers/cryptopanic_scraper.py
```

**Test CoinDesk:**

```bash
python scrapers/coindesk_scraper.py
```

---

### Test 3: Main Orchestrator (The Big One!)

```bash
python main.py
```

**Expected output:**

```
============================================================
🚀 CRYPTO SENTIMENT MONITOR - DATA COLLECTION
============================================================
⏰ Started at: 2024-12-30 15:45:23

📦 Initializing database...
✅ Database initialized successfully!

🐦 [1/3] Scraping Nitter (Twitter)...
------------------------------------------------------------
✅ Found working Nitter instance: nitter.poast.org
🔍 Scraping Nitter: https://...
📊 Found 50 tweets
✅ Successfully scraped 45 tweets from Nitter
✅ Nitter: 45 tweets collected

📰 [2/3] Scraping CryptoPanic (News)...
------------------------------------------------------------
🔍 Scraping CryptoPanic: https://cryptopanic.com/news/
📊 Found 60 potential news items
✅ Successfully scraped 40 news items from CryptoPanic
✅ CryptoPanic: 40 news items collected

📊 [3/3] Scraping CoinDesk (Professional News)...
------------------------------------------------------------
🔍 Scraping CoinDesk: https://www.coindesk.com/tag/markets/
📊 Found 35 potential articles
✅ Successfully scraped 30 unique articles from CoinDesk
✅ CoinDesk: 30 articles collected

============================================================
📊 COLLECTION SUMMARY
============================================================
🐦 Nitter (Twitter):     45 items
📰 CryptoPanic (News):   40 items
📊 CoinDesk (Articles):  30 items
------------------------------------------------------------
✅ Total collected:     115 items
============================================================

📈 DATABASE STATS
============================================================
Total entries in DB:     115
Analyzed:                  0
Pending analysis:        115
============================================================

⏰ Finished at: 2024-12-30 15:48:45

💡 Next steps:
   1. Run sentiment analysis: python -c "from analysis.sentiment_analyzer import process_unanalyzed_data; process_unanalyzed_data()"
   2. View dashboard: streamlit run dashboard/app.py
   3. Send report: python -c "from automation.email_reporter import send_weekly_report; send_weekly_report()"
```

---

## 🐛 Troubleshooting

### Problem: "No module named 'utils'"

**Solution:** Make sure you're running from the project root directory and `__init__.py` files exist

### Problem: "No working Nitter instances found"

**Solution:** Nitter instances go down sometimes. Wait a bit or we can add more instances to config

### Problem: ImportError for BeautifulSoup

**Solution:**

```bash
pip install beautifulsoup4 requests lxml
```

### Problem: Database locked error

**Solution:** Close any programs that might be accessing the database, or delete `data/crypto_sentiment.db` and run again

### Problem: Scrapers return 0 items

**Solution:**

- Check your internet connection
- Website might have changed structure (normal for web scraping)
- Try running individual scrapers to see which one fails

---

## ✅ Verification Checklist

Before sending to your friend, verify:

- [ ] `python main.py` runs without errors
- [ ] Database file created at `data/crypto_sentiment.db`
- [ ] At least 50+ total items collected
- [ ] All 3 sources have data (Nitter, CryptoPanic, CoinDesk)
- [ ] Check database has data:

```bash
python -c "from utils.database import get_all_data; print(len(get_all_data()))"
```

---

## 📦 What to Send Your Friend

Send your friend these files:

1. `utils/database.py`
2. `utils/config.py`
3. `data/crypto_sentiment.db` (after you've collected data)
4. The requirements document you already sent

Your friend should NOT receive:

- Scraper files (they don't need them)
- main.py (they don't need it)

---

## 🔄 Data Collection Schedule

**For this week (tight deadline):**

Run `python main.py` at these times:

- Day 1: Run 3 times (morning, afternoon, evening)
- Day 2: Run 3 times
- Day 3: Run 2 times
- Day 4: Run 2 times

This gives you ~10 runs × 100+ items = 1000+ data points for analysis!

**Quick collection command:**

```bash
# Run collection, wait 3 hours, run again (repeat)
python main.py && sleep 10800 && python main.py
```

---

## 🎯 Success Criteria

Your part is successful if:

1. ✅ `main.py` collects 100+ items per run
2. ✅ Database has data from all 3 sources
3. ✅ No critical errors during scraping
4. ✅ Database file can be opened and read
5. ✅ Your friend can import and use `utils.database` functions

---

## 🚨 Common Issues & Fixes

### Issue: Scrapers are slow

**Normal!** Web scraping has delays to be polite. Each run takes 2-5 minutes.

### Issue: Some scrapers fail

**Normal!** Websites go down or block scrapers. As long as 2/3 work, you're good.

### Issue: Duplicate data

**Not a problem!** We can filter duplicates later in analysis.

### Issue: Timestamps are all "now"

**Expected!** Some sites don't show exact times, we use current time as fallback.

---

## 💪 You're Ready!

If all tests pass, you're DONE with your part! 🎉

Next: Your friend builds analysis/dashboard while you keep collecting data.

When you merge: Just drop their `analysis/`, `dashboard/`, `automation/` folders into your project and everything will work! 🚀
