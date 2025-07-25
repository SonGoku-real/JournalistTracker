"""
Script to fetch and update the crypto news feed.
Can be run manually or scheduled via cron.

Usage:
    python refresh_news.py [--days=1] [--analyze=true]
"""

import os
import sys
import logging
import requests
from datetime import datetime, timedelta
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Parse command line arguments
parser = argparse.ArgumentParser(description='Refresh cryptocurrency news feed')
parser.add_argument('--days', type=int, default=1, help='Number of days to look back for articles')
parser.add_argument('--limit', type=int, default=10, help='Maximum number of articles to process')
parser.add_argument('--analyze', type=str, default='false', help='Whether to analyze content with OpenAI (true/false)')
args = parser.parse_args()

# News API configuration
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

# List of cryptocurrency keywords to track
CRYPTO_KEYWORDS = [
    "bitcoin", "ethereum", "cryptocurrency", "blockchain", "web3",
    "crypto", "defi", "nft", "token", "coinbase", "binance"
]

def fetch_latest_crypto_news(days=1, limit=10):
    """
    Fetch the latest cryptocurrency news articles using the News API.
    
    Args:
        days (int): Number of days to look back for articles
        limit (int): Maximum number of articles to return
        
    Returns:
        list: List of news articles as dictionaries
    """
    if not NEWS_API_KEY:
        logger.error("NEWS_API_KEY not found in environment variables")
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
        
        logger.info(f"Fetching news from {from_date} to now")
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        if data.get('status') != 'ok':
            logger.error(f"API returned error: {data.get('message', 'Unknown error')}")
            return []
            
        articles = data.get('articles', [])
        logger.info(f"Found {len(articles)} articles, processing up to {limit}")
        return articles[:limit]  # Limit the number of articles
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []

def main():
    # Convert analyze arg from string to boolean
    analyze_content = args.analyze.lower() == 'true'
    
    # Import necessary modules (delayed import to avoid circular imports)
    from flask import Flask
    from app import db, app
    from models import Article, Journalist, Outlet, Topic
    
    # Fetch the latest crypto news
    articles = fetch_latest_crypto_news(days=args.days, limit=args.limit)
    if not articles:
        logger.warning("No articles found or API error occurred")
        return 0
    
    # Process and add articles to the database
    with app.app_context():
        articles_added = 0
        
        for article_data in articles:
            # Skip if missing critical fields
            if not all(k in article_data for k in ['title', 'url', 'publishedAt']):
                continue
                
            # Check if article already exists
            existing = Article.query.filter_by(url=article_data['url']).first()
            if existing:
                continue
                
            # Get or create outlet
            source_name = article_data.get('source', {}).get('name', 'Unknown Source')
            logger.info(f"Processing article from {source_name}")
            
            outlet = Outlet.query.filter_by(name=source_name).first()
            if not outlet:
                outlet = Outlet(
                    name=source_name,
                    website=None,
                    country=None,
                    description=f"Crypto news outlet: {source_name}",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(outlet)
                db.session.flush()
            
            # Get or create journalist
            author = article_data.get('author', 'Unknown Author')
            journalist = Journalist.query.filter_by(name=author).first()
            if not journalist:
                journalist = Journalist(
                    name=author,
                    outlet_id=outlet.id,
                    region='Unknown',  # Default region
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(journalist)
                db.session.flush()
            
            # Parse published date
            try:
                published_at = datetime.strptime(article_data['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                published_at = datetime.utcnow()
            
            # Create article
            article = Article(
                title=article_data['title'],
                url=article_data['url'],
                content=article_data.get('description', ''),
                published_at=published_at,
                journalist_id=journalist.id,
                outlet_id=outlet.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                sentiment_score=0.0,
                sentiment_label='neutral'
            )
            
            # Try to extract topics from keywords
            crypto_topics = {
                'Bitcoin': ['bitcoin', 'btc'],
                'Ethereum': ['ethereum', 'eth'],
                'DeFi': ['defi', 'decentralized finance'],
                'NFT': ['nft', 'non-fungible'],
                'Regulation': ['regulation', 'sec', 'compliance', 'legal'],
                'Mining': ['mining', 'miner'],
                'Exchanges': ['exchange', 'trading', 'binance', 'coinbase'],
                'Cryptocurrency': ['cryptocurrency', 'crypto']
            }
            
            article_text = (article_data.get('title', '') + ' ' + 
                           article_data.get('description', '')).lower()
            
            # Get or create topics and add to article
            for topic_name, keywords in crypto_topics.items():
                if any(keyword in article_text for keyword in keywords):
                    # Look up topic
                    topic = Topic.query.filter_by(name=topic_name).first()
                    if not topic:
                        # Create topic if it doesn't exist
                        topic = Topic(
                            name=topic_name,
                            created_at=datetime.utcnow(),
                            updated_at=datetime.utcnow()
                        )
                        db.session.add(topic)
                        db.session.flush()
                    
                    # Add topic to article
                    article.topics.append(topic)
            
            # Add article to database
            db.session.add(article)
            articles_added += 1
        
        # Commit all changes if any articles were added
        if articles_added > 0:
            db.session.commit()
            logger.info(f"Added {articles_added} new articles to the database")
        else:
            logger.info("No new articles to add")
            
        return articles_added

if __name__ == "__main__":
    count = main()
    print(f"Added {count} new articles to the database")