"""Database utility functions"""

import sqlite3
from utils.config import DB_PATH

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

def get_unanalyzed_data():
    """Returns list of dicts for rows where sentiment_score IS NULL"""
    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, source, content, timestamp, url, engagement_score
            FROM scraped_data
            WHERE sentiment_score IS NULL
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error in get_unanalyzed_data: {e}")
        return []

def update_sentiment(row_id, sentiment_score, sentiment_label, crypto_mentioned):
    """Updates a row with analysis results"""
    try:
        conn = get_connection()
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
        print(f"Error in update_sentiment: {e}")
        return False

def get_data_by_timerange(hours=24):
    """Returns all analyzed data from last X hours"""
    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT *
            FROM scraped_data
            WHERE datetime(timestamp) >= datetime('now', '-' || ? || ' hours')
            ORDER BY timestamp DESC
        ''', (hours,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error in get_data_by_timerange: {e}")
        return []

def get_all_data():
    """Returns ALL rows from database"""
    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM scraped_data ORDER BY timestamp DESC')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error in get_all_data: {e}")
        return []