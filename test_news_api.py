"""
Simple script to test the News API directly.
"""

import os
import json
import requests
from datetime import datetime, timedelta

# News API configuration
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

# List of cryptocurrency keywords to track
CRYPTO_KEYWORDS = [
    "bitcoin", "ethereum", "cryptocurrency", "blockchain", "web3",
    "crypto", "defi", "nft", "token", "coinbase", "binance"
]

def fetch_crypto_news(days=3):
    """Fetch the latest crypto news directly from News API."""
    if not NEWS_API_KEY:
        print("ERROR: NEWS_API_KEY not found in environment variables")
        return []
    
    # Format the date for the API (looking back X days)
    from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    # Create a query string from the keywords (joined with OR)
    query = " OR ".join(CRYPTO_KEYWORDS)
    
    try:
        params = {
            'q': query,
            'from': from_date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': NEWS_API_KEY
        }
        
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        if data.get('status') != 'ok':
            print(f"ERROR: API returned error: {data.get('message', 'Unknown error')}")
            return []
            
        return data.get('articles', [])
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Error fetching news: {e}")
        return []
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return []

if __name__ == "__main__":
    print(f"Testing News API with key: {NEWS_API_KEY[:4]}...{NEWS_API_KEY[-4:] if NEWS_API_KEY else 'None'}")
    articles = fetch_crypto_news(days=3)
    print(f"Found {len(articles)} articles")
    
    if articles:
        print("\nSample articles:")
        for i, article in enumerate(articles[:5]):
            print(f"{i+1}. {article['title']}")
            print(f"   Source: {article['source']['name']}")
            print(f"   Date: {article['publishedAt']}")
            print(f"   URL: {article['url']}")
            print()
            
        # Save all articles to a JSON file for inspection
        with open('crypto_news.json', 'w') as f:
            json.dump(articles, f, indent=2)
        print(f"Saved all {len(articles)} articles to crypto_news.json")