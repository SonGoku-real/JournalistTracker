"""
Script to fetch the latest cryptocurrency news and save it to the database.
This script avoids circular imports by creating a standalone environment.
"""

import os
import json
import logging
import requests
from datetime import datetime, timedelta
import importlib

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        logger.info(f"Found {len(articles)} articles")
        return articles
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []

def update_database_with_articles():
    """Fetch articles and update the database."""
    # Import Flask app and models here to avoid circular imports
    from flask import Flask
    from app import db
    from models import Article, Journalist, Outlet, Topic
    from app import app
    
    articles = fetch_crypto_news(days=3)
    if not articles:
        logger.warning("No articles found to import")
        return 0
    
    articles_added = 0
    with app.app_context():
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
                    website=None,  # We don't have the website URL from the API
                    country=None,  # We don't have country info
                    description=f"Crypto news outlet: {source_name}",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(outlet)
                db.session.flush()  # Get ID without committing
            
            # Get or create journalist
            author = article_data.get('author', 'Unknown Author')
            journalist = Journalist.query.filter_by(name=author).first()
            if not journalist:
                journalist = Journalist(
                    name=author,
                    outlet_id=outlet.id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(journalist)
                db.session.flush()  # Get ID without committing
            
            # Parse published date
            try:
                published_at = datetime.strptime(article_data['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                published_at = datetime.utcnow()
            
            # Create article
            article = Article(
                title=article_data['title'],
                url=article_data['url'],
                content=article_data.get('description', ''),  # Use description initially
                published_at=published_at,
                journalist_id=journalist.id,
                outlet_id=outlet.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                # Set default sentiment (can be updated later with OpenAI)
                sentiment_score=0.0,
                sentiment_label='neutral'
            )
            
            # Assign topics based on keywords found in title/description
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
            
            # Check article title and description for keywords
            search_text = (article_data.get('title', '') + ' ' + article_data.get('description', '')).lower()
            
            for topic_name, keywords in crypto_topics.items():
                for keyword in keywords:
                    if keyword.lower() in search_text:
                        # Get or create topic
                        topic = Topic.query.filter_by(name=topic_name).first()
                        if not topic:
                            topic = Topic(
                                name=topic_name,
                                created_at=datetime.utcnow(),
                                updated_at=datetime.utcnow()
                            )
                            db.session.add(topic)
                            db.session.flush()
                        
                        # Add topic to article
                        article.topics.append(topic)
                        break  # Once we find one keyword match, move to next topic
            
            # Add and commit
            db.session.add(article)
            articles_added += 1
            logger.info(f"Added article: {article.title}")
        
        if articles_added > 0:
            db.session.commit()
            logger.info(f"Successfully added {articles_added} new articles")
        
        return articles_added

if __name__ == "__main__":
    logger.info("Starting crypto news update process")
    count = update_database_with_articles()
    logger.info(f"Added {count} new real crypto articles to the database")