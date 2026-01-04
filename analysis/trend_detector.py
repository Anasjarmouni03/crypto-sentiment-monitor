"""
Trend Detection Module
Identifies trending cryptocurrencies and sentiment patterns
"""

from utils.database import get_data_by_timerange
from collections import defaultdict


def get_trending_cryptos(hours: int = 24) -> list:
    """
    Get most mentioned cryptocurrencies in timeframe
    
    Args:
        hours (int): Lookback period
    
    Returns:
        list of dicts sorted by mentions (descending):
        [
            {
                'crypto': 'BTC',
                'mentions': 45,
                'avg_sentiment': 0.62,
                'positive_count': 30,
                'negative_count': 10,
                'neutral_count': 5
            },
            ...
        ]
    """
    try:
        # Get data from database
        data = get_data_by_timerange(hours)
        
        if not data:
            return []
        
        # Track crypto statistics
        crypto_stats = defaultdict(lambda: {
            'mentions': 0,
            'total_sentiment': 0.0,
            'positive': 0,
            'negative': 0,
            'neutral': 0
        })
        
        # Process each row
        for row in data:
            crypto_mentioned = row.get('crypto_mentioned', '')
            sentiment_score = row.get('sentiment_score')
            sentiment_label = row.get('sentiment_label', 'neutral')
            
            # Skip if no cryptos or no sentiment
            if not crypto_mentioned or sentiment_score is None:
                continue
            
            # Parse comma-separated cryptos
            cryptos = [c.strip() for c in crypto_mentioned.split(',') if c.strip()]
            
            for crypto in cryptos:
                crypto_stats[crypto]['mentions'] += 1
                crypto_stats[crypto]['total_sentiment'] += sentiment_score
                
                if sentiment_label == 'positive':
                    crypto_stats[crypto]['positive'] += 1
                elif sentiment_label == 'negative':
                    crypto_stats[crypto]['negative'] += 1
                else:
                    crypto_stats[crypto]['neutral'] += 1
        
        # Build result list
        result = []
        for crypto, stats in crypto_stats.items():
            avg_sentiment = stats['total_sentiment'] / stats['mentions'] if stats['mentions'] > 0 else 0.0
            result.append({
                'crypto': crypto,
                'mentions': stats['mentions'],
                'avg_sentiment': round(avg_sentiment, 2),
                'positive_count': stats['positive'],
                'negative_count': stats['negative'],
                'neutral_count': stats['neutral']
            })
        
        # Sort by mentions (descending) and return top 10
        result.sort(key=lambda x: x['mentions'], reverse=True)
        return result[:10]
        
    except Exception as e:
        print(f"Error in get_trending_cryptos: {e}")
        return []


def get_sentiment_by_source(hours: int = 24) -> dict:
    """
    Get average sentiment per source platform
    
    Args:
        hours (int): Lookback period
    
    Returns:
        dict: {
            'nitter': 0.35,
            'cryptopanic': 0.12,
            'coindesk': -0.08
        }
    """
    try:
        # Get data from database
        data = get_data_by_timerange(hours)
        
        # Initialize all sources to 0
        source_stats = {
            'nitter': {'total': 0.0, 'count': 0},
            'cryptopanic': {'total': 0.0, 'count': 0},
            'coindesk': {'total': 0.0, 'count': 0}
        }
        
        # Process each row
        for row in data:
            source = row.get('source')
            sentiment_score = row.get('sentiment_score')
            
            # Skip if no sentiment score or unknown source
            if sentiment_score is None or source not in source_stats:
                continue
            
            source_stats[source]['total'] += sentiment_score
            source_stats[source]['count'] += 1
        
        # Calculate averages
        result = {}
        for source, stats in source_stats.items():
            if stats['count'] > 0:
                result[source] = round(stats['total'] / stats['count'], 2)
            else:
                result[source] = 0.0
        
        return result
        
    except Exception as e:
        print(f"Error in get_sentiment_by_source: {e}")
        return {'nitter': 0.0, 'cryptopanic': 0.0, 'coindesk': 0.0}


def detect_sentiment_shift(current_hours: int = 6, compare_hours: int = 24) -> dict:
    """
    Detect if sentiment has shifted significantly
    
    Args:
        current_hours (int): Recent period
        compare_hours (int): Comparison period
    
    Returns:
        dict: {
            'current_sentiment': 0.45,
            'previous_sentiment': 0.12,
            'change': 0.33,
            'shift_direction': 'positive',  # or 'negative' or 'stable'
            'is_significant': True          # if abs(change) > 0.2
        }
    """
    try:
        # Get current period data
        current_data = get_data_by_timerange(current_hours)
        
        # Get comparison period data (excluding current period)
        all_data = get_data_by_timerange(compare_hours)
        
        # Calculate current sentiment
        current_sentiment = 0.0
        if current_data:
            current_scores = [row.get('sentiment_score', 0) for row in current_data 
                            if row.get('sentiment_score') is not None]
            if current_scores:
                current_sentiment = sum(current_scores) / len(current_scores)
        
        # Calculate previous sentiment (exclude current period)
        previous_sentiment = 0.0
        if all_data:
            # Get timestamps to filter out current period
            from datetime import datetime, timedelta
            current_cutoff = datetime.now() - timedelta(hours=current_hours)
            
            previous_scores = []
            for row in all_data:
                timestamp_str = row.get('timestamp')
                sentiment_score = row.get('sentiment_score')
                
                if sentiment_score is None:
                    continue
                
                # Parse timestamp and check if it's in previous period
                try:
                    if timestamp_str:
                        timestamp = datetime.fromisoformat(timestamp_str)
                        if timestamp < current_cutoff:
                            previous_scores.append(sentiment_score)
                except:
                    continue
            
            if previous_scores:
                previous_sentiment = sum(previous_scores) / len(previous_scores)
        
        # Calculate change
        change = current_sentiment - previous_sentiment
        
        # Determine shift direction
        if change > 0.05:
            shift_direction = 'positive'
        elif change < -0.05:
            shift_direction = 'negative'
        else:
            shift_direction = 'stable'
        
        # Check if significant
        is_significant = abs(change) > 0.2
        
        return {
            'current_sentiment': round(current_sentiment, 2),
            'previous_sentiment': round(previous_sentiment, 2),
            'change': round(change, 2),
            'shift_direction': shift_direction,
            'is_significant': is_significant
        }
        
    except Exception as e:
        print(f"Error in detect_sentiment_shift: {e}")
        return {
            'current_sentiment': 0.0,
            'previous_sentiment': 0.0,
            'change': 0.0,
            'shift_direction': 'stable',
            'is_significant': False
        }


if __name__ == "__main__":
    # Test the module
    print("Testing trend detector...\n")
    
    print("--- Trending Cryptos (24h) ---")
    trending = get_trending_cryptos(24)
    if trending:
        for i, crypto in enumerate(trending, 1):
            print(f"{i}. {crypto['crypto']}: {crypto['mentions']} mentions, "
                  f"avg sentiment: {crypto['avg_sentiment']}")
    else:
        print("No trending cryptos found")
    
    print("\n--- Sentiment by Source (24h) ---")
    by_source = get_sentiment_by_source(24)
    for source, sentiment in by_source.items():
        print(f"{source}: {sentiment}")
    
    print("\n--- Sentiment Shift Detection ---")
    shift = detect_sentiment_shift(6, 24)
    print(f"Current: {shift['current_sentiment']}")
    print(f"Previous: {shift['previous_sentiment']}")
    print(f"Change: {shift['change']}")
    print(f"Direction: {shift['shift_direction']}")
    print(f"Significant: {shift['is_significant']}")