"""
Analysis package for crypto sentiment monitoring
Contains sentiment analysis and trend detection modules
"""

from .sentiment_analyzer import analyze_sentiment, detect_cryptos, process_unanalyzed_data
from .trend_detector import get_trending_cryptos, get_sentiment_by_source, detect_sentiment_shift

__all__ = [
    'analyze_sentiment',
    'detect_cryptos', 
    'process_unanalyzed_data',
    'get_trending_cryptos',
    'get_sentiment_by_source',
    'detect_sentiment_shift'
]