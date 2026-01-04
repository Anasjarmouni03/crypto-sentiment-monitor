"""
Simplified Main - Uses Universal Scraper
"""

from scrapers.universal_scraper import scrape_all
from utils.database import init_database, insert_scraped_data, get_stats
import os
import sys
from datetime import datetime

# Fix SSL
for var in ['SSL_CERT_FILE', 'REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE']:
    if var in os.environ:
        del os.environ[var]


def main():
    print("=" * 60)
    print("CRYPTO SENTIMENT MONITOR - SIMPLIFIED VERSION")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Initialize database
    init_database()

    # Scrape all sources
    all_data = scrape_all(limit_per_source=30)

    # Insert into database
    print("\nInserting into database...")
    stats = {'total': 0, 'errors': 0}

    for source, items in all_data.items():
        for item in items:
            try:
                success = insert_scraped_data(
                    source=source,
                    content=item['content'],
                    timestamp=item['timestamp'],
                    url=item['url'],
                    engagement=item['engagement']
                )
                if success:
                    stats['total'] += 1
                else:
                    stats['errors'] += 1
            except Exception as e:
                stats['errors'] += 1
                print(f"Error inserting: {str(e)[:50]}")

    print(f"Inserted {stats['total']} items into database")
    if stats['errors'] > 0:
        print(f"{stats['errors']} errors")

    # Show database stats
    print("\n" + "=" * 60)
    print("DATABASE STATS")
    print("=" * 60)
    db_stats = get_stats()
    print(f"Total entries: {db_stats.get('total', 0)}")
    print(f"Analyzed: {db_stats.get('analyzed', 0)}")
    print(f"Pending analysis: {db_stats.get('unanalyzed', 0)}")
    print(f"By source: {db_stats.get('by_source', {})}")
    print("=" * 60)

    print(f"\nFinished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return stats['total'] > 0


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
