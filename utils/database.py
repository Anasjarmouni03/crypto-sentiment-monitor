"""
Database Module for Crypto Sentiment Monitor
Handles all SQLite database operations
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import os

# Database path
DB_PATH = 'data/crypto_sentiment.db'


def init_database():
    """
    Initialize database and create tables if they don't exist
    Creates the scraped_data table with all required columns
    """
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create main table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scraped_data (
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
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


def insert_scraped_data(source: str, content: str, timestamp: str,
                        url: str, engagement: int = 0) -> bool:
    """
    Insert raw scraped data into database

    Args:
        source: Platform name ('nitter', 'cryptopanic', 'coindesk')
        content: Tweet/headline/article text
        timestamp: When content was published (string format)
        url: Source URL
        engagement: Likes/votes/shares count

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO scraped_data 
            (source, content, timestamp, url, engagement_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (source, content, timestamp, url, engagement))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return False


def get_unanalyzed_data() -> List[Dict]:
    """
    Get all rows where sentiment analysis hasn't been done yet

    Returns:
        List of dicts with unanalyzed data
        Format: [{'id': 1, 'source': 'nitter', 'content': '...', ...}, ...]
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Return rows as dicts
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, source, content, timestamp, url, engagement_score
            FROM scraped_data
            WHERE sentiment_score IS NULL
        ''')

        rows = cursor.fetchall()
        conn.close()

        # Convert to list of dicts
        result = [dict(row) for row in rows]
        return result

    except Exception as e:
        print(f"❌ Error fetching unanalyzed data: {e}")
        return []


def update_sentiment(row_id: int, sentiment_score: float,
                     sentiment_label: str, crypto_mentioned: str) -> bool:
    """
    Update a row with sentiment analysis results

    Args:
        row_id: The id from get_unanalyzed_data()
        sentiment_score: -1.0 to +1.0
        sentiment_label: 'positive', 'negative', or 'neutral'
        crypto_mentioned: Comma-separated crypto symbols (e.g., "BTC,ETH")

    Returns:
        bool: True if successful
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE scraped_data
            SET sentiment_score = ?,
                sentiment_label = ?,
                crypto_mentioned = ?
            WHERE id = ?
        ''', (sentiment_score, sentiment_label, crypto_mentioned, row_id))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Error updating sentiment for row {row_id}: {e}")
        return False


def get_data_by_timerange(hours: int = 24) -> List[Dict]:
    """
    Get all analyzed data from last X hours

    Args:
        hours: Number of hours to look back

    Returns:
        List of dicts with ALL columns including sentiment data
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT *
            FROM scraped_data
            WHERE sentiment_score IS NOT NULL
            AND datetime(timestamp) >= datetime('now', '-' || ? || ' hours')
            ORDER BY timestamp DESC
        ''', (hours,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    except Exception as e:
        print(f"❌ Error fetching data by timerange: {e}")
        return []


def get_all_data() -> List[Dict]:
    """
    Get ALL rows from database (analyzed and unanalyzed)

    Returns:
        List of all rows as dicts
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM scraped_data ORDER BY timestamp DESC')

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    except Exception as e:
        print(f"❌ Error fetching all data: {e}")
        return []


def get_stats() -> Dict:
    """
    Get database statistics

    Returns:
        Dict with stats: total rows, analyzed, unanalyzed, by source
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Total rows
        cursor.execute('SELECT COUNT(*) FROM scraped_data')
        total = cursor.fetchone()[0]

        # Analyzed rows
        cursor.execute(
            'SELECT COUNT(*) FROM scraped_data WHERE sentiment_score IS NOT NULL')
        analyzed = cursor.fetchone()[0]

        # By source
        cursor.execute('''
            SELECT source, COUNT(*) as count
            FROM scraped_data
            GROUP BY source
        ''')
        by_source = {row[0]: row[1] for row in cursor.fetchall()}

        conn.close()

        return {
            'total': total,
            'analyzed': analyzed,
            'unanalyzed': total - analyzed,
            'by_source': by_source
        }

    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return {}


# Initialize database on import
if __name__ == "__main__":
    init_database()
    print("\n📊 Database Stats:")
    stats = get_stats()
    print(f"Total entries: {stats.get('total', 0)}")
    print(f"Analyzed: {stats.get('analyzed', 0)}")
    print(f"Unanalyzed: {stats.get('unanalyzed', 0)}")
    print(f"By source: {stats.get('by_source', {})}")
