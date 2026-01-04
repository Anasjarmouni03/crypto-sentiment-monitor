"""
Universal Crypto Scraper - Bulletproof version
Combines all sources with better error handling
"""

import random
from typing import List, Dict
from datetime import datetime
import time
from bs4 import BeautifulSoup
import urllib3
import requests
import os
import sys

# FIX SSL FIRST - Before ANY imports
for var in ['SSL_CERT_FILE', 'REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE']:
    if var in os.environ:
        del os.environ[var]


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Rotate user agents to avoid blocks
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]


def get_headers():
    """Get random headers to avoid blocking"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }


def scrape_reddit(limit=50) -> List[Dict]:
    """Scrape Reddit with better anti-blocking"""
    results = []

    print("🔴 Scraping Reddit r/cryptocurrency...")

    # Try multiple subreddits
    subreddits = ['cryptocurrency', 'CryptoMarkets', 'Bitcoin']

    for subreddit in subreddits:
        if len(results) >= limit:
            break

        try:
            url = f'https://old.reddit.com/r/{subreddit}/.json?limit=25'

            headers = get_headers()
            headers['Accept'] = 'application/json'

            time.sleep(random.uniform(1, 3))  # Random delay

            response = requests.get(
                url, headers=headers, timeout=15, verify=False)

            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])

                for post in posts:
                    post_data = post.get('data', {})
                    title = post_data.get('title', '')
                    selftext = post_data.get('selftext', '')

                    content = f"{title}. {selftext}".strip()
                    if len(content) < 20:
                        content = title

                    if len(content) < 10:
                        continue

                    timestamp = datetime.fromtimestamp(
                        post_data.get('created_utc', time.time())
                    ).strftime('%Y-%m-%d %H:%M:%S')

                    results.append({
                        'content': content[:500],
                        'timestamp': timestamp,
                        'engagement': post_data.get('score', 0),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}"
                    })

                    if len(results) >= limit:
                        break

                print(
                    f"  ✅ r/{subreddit}: {len([r for r in results if subreddit in r['url']])} posts")

        except Exception as e:
            print(f"  ⚠️ r/{subreddit}: {str(e)[:50]}")
            continue

    return results[:limit]


def scrape_cryptonews_io(limit=20) -> List[Dict]:
    """Scrape cryptonews.io - simpler structure"""
    results = []

    print("📰 Scraping CryptoNews.io...")

    try:
        url = 'https://cryptonews.com/'
        response = requests.get(
            url, headers=get_headers(), timeout=15, verify=False)

        if response.status_code != 200:
            return results

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find article links
        articles = soup.find_all('a', href=True, limit=limit*3)

        for article in articles:
            if len(results) >= limit:
                break

            try:
                # Get text content
                text = article.get_text(strip=True)

                # Skip short texts and navigation
                if len(text) < 30 or any(skip in text.lower() for skip in
                                         ['menu', 'login', 'subscribe', 'more', 'read']):
                    continue

                href = article.get('href', '')
                if not href.startswith('http'):
                    href = 'https://cryptonews.com' + href

                # Skip non-article links
                if any(skip in href for skip in ['#', 'javascript', 'category', 'tag', 'author']):
                    continue

                results.append({
                    'content': text[:300],
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'engagement': 0,
                    'url': href
                })

            except:
                continue

        print(f"  ✅ Found {len(results)} articles")

    except Exception as e:
        print(f"  ❌ Error: {str(e)[:50]}")

    return results


def scrape_cointelegraph(limit=20) -> List[Dict]:
    """Scrape Cointelegraph"""
    results = []

    print("📊 Scraping Cointelegraph...")

    try:
        url = 'https://cointelegraph.com/tags/bitcoin'
        response = requests.get(
            url, headers=get_headers(), timeout=15, verify=False)

        if response.status_code != 200:
            return results

        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for article titles
        titles = soup.find_all(['h1', 'h2', 'h3', 'h4'], limit=limit*2)

        for title_elem in titles:
            if len(results) >= limit:
                break

            try:
                title = title_elem.get_text(strip=True)

                if len(title) < 30:
                    continue

                # Get parent link
                link = title_elem.find_parent('a')
                url_link = 'https://cointelegraph.com'

                if link and link.get('href'):
                    url_link = link.get('href')
                    if not url_link.startswith('http'):
                        url_link = 'https://cointelegraph.com' + url_link

                results.append({
                    'content': title,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'engagement': 0,
                    'url': url_link
                })

            except:
                continue

        print(f"  ✅ Found {len(results)} articles")

    except Exception as e:
        print(f"  ❌ Error: {str(e)[:50]}")

    return results


def scrape_all(limit_per_source=30) -> Dict[str, List[Dict]]:
    """
    Scrape all sources and return organized data

    Returns:
        Dict with source names as keys and lists of scraped data as values
    """
    all_data = {}

    print("=" * 60)
    print("🚀 UNIVERSAL CRYPTO SCRAPER")
    print("=" * 60)
    print()

    # Reddit (most reliable)
    reddit_data = scrape_reddit(limit=limit_per_source)
    if reddit_data:
        all_data['reddit'] = reddit_data
    print()

    # CryptoNews.io
    cryptonews_data = scrape_cryptonews_io(limit=limit_per_source)
    if cryptonews_data:
        all_data['cryptonews'] = cryptonews_data
    print()

    # Cointelegraph
    ct_data = scrape_cointelegraph(limit=limit_per_source)
    if ct_data:
        all_data['cointelegraph'] = ct_data
    print()

    # Summary
    total = sum(len(items) for items in all_data.values())
    print("=" * 60)
    print(f"✅ TOTAL COLLECTED: {total} items")
    for source, items in all_data.items():
        print(f"   {source}: {len(items)} items")
    print("=" * 60)

    return all_data


if __name__ == "__main__":
    data = scrape_all()
