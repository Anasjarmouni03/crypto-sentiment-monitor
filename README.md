# ⚡ Crypto Sentiment Monitor

> **Real-time AI-powered sentiment analysis for the cryptocurrency market.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b)
![Status](https://img.shields.io/badge/Status-Live-success)

## 📖 Overview

The **Crypto Sentiment Monitor** is an advanced analytics platform that tracks, analyzes, and visualizes market sentiment across multiple data sources in real-time. By scraping data from **Reddit**, **CryptoNews**, and **Cointelegraph**, it uses Natural Language Processing (VADER) to determine whether the market mood is Bullish 🟢, Bearish 🔴, or Neutral ⚪.

Designed with a **"Live Command Center"** aesthetic, the dashboard features a premium dark-mode UI, neon-glowing charts, and AI-generated market insights, making it the perfect tool for traders and analysts.

---

## ✨ Key Features

### 🖥️ Premium Live Dashboard
*   **Real-Time News Ticker**: Scrolling marquee of the latest headlines with sentiment indicators.
*   **AI Market Insights**: Smart, natural-language summaries of the current market state (e.g., *"Bitcoin is surging..."*).
*   **Neon Glassmorphism UI**: Modern, dark-themed interface with blurred glass cards and glowing charts.
*   **Topic Radar**: Dynamic tag cloud visualizing the most talked-about topics (e.g., "ETF", "Crash", "Moon").
*   **Demo Mode**: Built-in simulation toggle to showcase live data flow for presentations.

### 🤖 Intelligent Automation
*   **Universal Scraper**: robustly collects data from Reddit, CryptoNews, and Cointelegraph.
*   **Automated Scheduler**: Background process that scrapes and analyzes data every **15 minutes**.
*   **Sentiment Engine**: VADER-based analysis to score and label every piece of content.
*   **Weekly Reports**: Automated email summaries sent every Monday morning.

---

## 🚀 Quick Start Guide

### 1. Installation
Clone the repository and install the required dependencies:

```bash
git clone https://github.com/Anasjarmouni03/crypto-sentiment-monitor.git
cd crypto-sentiment-monitor
pip install -r requirements.txt
```

### 2. Run the Dashboard
Launch the visual interface:

```bash
streamlit run dashboard/app.py
```
*Access the dashboard at `http://localhost:8501`*

### 3. Start Automation (Optional)
To enable background scraping and analysis:

```bash
python automation/scheduler.py
```
*This will run in the background, updating the database every 15 minutes.*

---

## 📂 Project Structure

```
crypto-sentiment-monitor/
├── 📊 dashboard/          # Streamlit frontend application
│   └── app.py            # Main dashboard entry point
├── 🤖 automation/         # Background tasks
│   ├── scheduler.py      # Orchestrates scraping & analysis
│   └── email_reporter.py # Handles weekly email summaries
├── 🕷️ scrapers/           # Data collection modules
│   └── universal_scraper.py
├── 🧠 analysis/           # NLP & Logic
│   ├── sentiment_analyzer.py
│   └── trend_detector.py
├── 💾 data/               # SQLite database storage
└── ⚙️ utils/              # Database & Config helpers
```

---

## 🛠️ Technologies Used

*   **Frontend**: Streamlit, Plotly (Interactive Charts), HTML/CSS (Custom Styling)
*   **Backend**: Python, APScheduler (Automation)
*   **Data**: SQLite, Pandas
*   **NLP**: VADER Sentiment Analysis
*   **Scraping**: BeautifulSoup4, Requests

---

## 🔮 Future Roadmap

*   [ ] Integration with Twitter/X API for broader social coverage.
*   [ ] Price correlation analysis (Sentiment vs. Price Action).
*   [ ] User alerts via Telegram/Discord bots.

---

*Built for the ENSET Python Project.*
