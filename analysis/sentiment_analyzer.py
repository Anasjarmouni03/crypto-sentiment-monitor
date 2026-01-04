"""
Sentiment Analysis Module
Analyzes sentiment and detects cryptocurrencies in scraped content
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils.config import CRYPTO_LIST
from utils.database import get_unanalyzed_data, update_sentiment
import re


def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of text using VADER
    
    Args:
        text (str): Content to analyze
    
    Returns:
        dict: {
            'score': float,      # -1.0 to +1.0
            'label': str         # 'positive', 'negative', or 'neutral'
        }
    """
    try:
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        compound_score = scores['compound']
        
        # Determine label based on threshold
        if compound_score > 0.05:
            label = 'positive'
        elif compound_score < -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        
        return {
            'score': compound_score,
            'label': label
        }
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return {'score': 0.0, 'label': 'neutral'}


def detect_cryptos(text: str) -> str:
    """
    Detect cryptocurrencies mentioned in text
    
    Args:
        text (str): Content to search
    
    Returns:
        str: Comma-separated crypto symbols, e.g., "BTC,ETH,SOL"
             Empty string if none found
    """
    try:
        found_cryptos = set()
        text_upper = text.upper()
        
        # Map full names to symbols
        crypto_map = {
            'BITCOIN': 'BTC',
            'ETHEREUM': 'ETH',
            'SOLANA': 'SOL',
            'CARDANO': 'ADA',
            'RIPPLE': 'XRP',
            'DOGECOIN': 'DOGE',
            'POLYGON': 'MATIC',
            'POLKADOT': 'DOT',
            'AVALANCHE': 'AVAX',
            'CHAINLINK': 'LINK'
        }
        
        # Check each crypto in the list
        for crypto in CRYPTO_LIST:
            crypto_upper = crypto.upper()
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(crypto_upper) + r'\b'
            if re.search(pattern, text_upper):
                # If it's a full name, convert to symbol
                if crypto_upper in crypto_map:
                    found_cryptos.add(crypto_map[crypto_upper])
                else:
                    # It's already a symbol
                    found_cryptos.add(crypto_upper)
        
        # Return sorted, comma-separated string
        return ','.join(sorted(found_cryptos))
    
    except Exception as e:
        print(f"Error detecting cryptos: {e}")
        return ""


def process_unanalyzed_data():
    """
    Main processing function - analyzes all unanalyzed data
    
    Process:
        1. Get unanalyzed data using get_unanalyzed_data()
        2. For each row:
           a. Analyze sentiment
           b. Detect cryptos
           c. Update database using update_sentiment()
        3. Print progress: "Analyzed X entries"
    
    Returns:
        int: Number of entries processed
    """
    try:
        # Get unanalyzed data from database
        unanalyzed_data = get_unanalyzed_data()
        
        if not unanalyzed_data:
            print("No unanalyzed data found")
            return 0
        
        processed_count = 0
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for row in unanalyzed_data:
            try:
                # Extract data
                row_id = row['id']
                content = row['content']
                
                # Analyze sentiment
                sentiment_result = analyze_sentiment(content)
                sentiment_score = sentiment_result['score']
                sentiment_label = sentiment_result['label']
                
                # Detect cryptocurrencies
                crypto_mentioned = detect_cryptos(content)
                
                # Update database
                success = update_sentiment(
                    row_id=row_id,
                    sentiment_score=sentiment_score,
                    sentiment_label=sentiment_label,
                    crypto_mentioned=crypto_mentioned
                )
                
                if success:
                    processed_count += 1
                    if sentiment_label == 'positive':
                        positive_count += 1
                    elif sentiment_label == 'negative':
                        negative_count += 1
                    else:
                        neutral_count += 1
                else:
                    print(f"Failed to update row {row_id}")
                    
            except Exception as e:
                print(f"Error processing row {row.get('id', 'unknown')}: {e}")
                continue
        
        # Print summary
        print(f"Analyzed {processed_count} entries")
        print(f"- Positive: {positive_count}")
        print(f"- Negative: {negative_count}")
        print(f"- Neutral: {neutral_count}")
        
        return processed_count
        
    except Exception as e:
        print(f"Error in process_unanalyzed_data: {e}")
        return 0


if __name__ == "__main__":
    # Test the module
    print("Testing sentiment analyzer...")
    
    # Test analyze_sentiment
    test_texts = [
        "Bitcoin is amazing! Going to the moon! 🚀",
        "Ethereum is crashing, this is terrible",
        "Solana price remains stable today"
    ]
    
    print("\n--- Sentiment Analysis Tests ---")
    for text in test_texts:
        result = analyze_sentiment(text)
        print(f"Text: {text}")
        print(f"Result: {result}\n")
    
    # Test detect_cryptos
    print("--- Crypto Detection Tests ---")
    test_crypto_texts = [
        "BTC and ETH are pumping!",
        "Bitcoin, Ethereum, and Solana all up today",
        "No cryptos mentioned here",
        "DOGE to the moon with BTC"
    ]
    
    for text in test_crypto_texts:
        cryptos = detect_cryptos(text)
        print(f"Text: {text}")
        print(f"Detected: {cryptos}\n")
    
    # Process unanalyzed data
    print("--- Processing Unanalyzed Data ---")
    count = process_unanalyzed_data()
    print(f"\nTotal processed: {count}")