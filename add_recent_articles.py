"""
Script to add the most recent crypto articles to the database.
This is a simpler approach that minimizes the risk of circular imports.
"""

import os
import json
import logging
import requests
from datetime import datetime, timedelta
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def add_recent_articles():
    """
    Add articles from January-March 2024 to provide 3 months of data for analysis.
    """
    # Import Flask app and models inside the function to avoid circular imports
    from app import app, db
    from models import Article, Journalist, Outlet, Topic
    
    # News API configuration
    NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
    if not NEWS_API_KEY:
        logger.error("NEWS_API_KEY environment variable not found")
        return False
    
    # List of cryptocurrency keywords
    crypto_keywords = [
        "bitcoin", "ethereum", "cryptocurrency", "blockchain", "web3",
        "crypto", "defi", "nft", "token"
    ]
    
    # Create query string (joined with OR)
    query = " OR ".join(crypto_keywords)
    
    # Look back 3 days maximum
    from_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    
    # News API endpoint
    url = "https://newsapi.org/v2/everything"
    
    # Request parameters
    params = {
        'q': query,
        'from': from_date,
        'sortBy': 'publishedAt',
        'language': 'en',
        'apiKey': NEWS_API_KEY
    }
    
    logger.info(f"Fetching news from {from_date} to now")
    
    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Parse the response
        data = response.json()
        
        if data.get('status') != 'ok':
            logger.error(f"API returned error: {data.get('message', 'Unknown error')}")
            return False
        
        articles = data.get('articles', [])
        logger.info(f"Found {len(articles)} articles")
        
        # Get the first 20 articles max to avoid timeouts
        articles = articles[:20]
        
        # Use app context to interact with the database
        with app.app_context():
            # Process each article
            articles_added = 0
            
            for article_data in articles:
                # Skip if missing critical fields
                if not all(k in article_data for k in ['title', 'url', 'publishedAt']):
                    continue
                
                # Check if article already exists (by URL)
                existing = Article.query.filter_by(url=article_data['url']).first()
                if existing:
                    logger.info(f"Article already exists: {article_data['title']}")
                    continue
                
                # Get source name
                source_name = article_data.get('source', {}).get('name', 'Unknown Source')
                
                # Get or create outlet
                outlet = Outlet.query.filter_by(name=source_name).first()
                if not outlet:
                    logger.info(f"Creating new outlet: {source_name}")
                    outlet = Outlet(
                        name=source_name,
                        website=None,
                        country=None,
                        description=f"News source: {source_name}"
                    )
                    db.session.add(outlet)
                    # Flush to get the ID without committing
                    db.session.flush()
                
                # Get or create journalist
                author = article_data.get('author', 'Unknown Author')
                journalist = Journalist.query.filter_by(name=author).first()
                if not journalist:
                    logger.info(f"Creating new journalist: {author}")
                    journalist = Journalist(
                        name=author,
                        outlet_id=outlet.id,
                        region='Unknown'  # Default region
                    )
                    db.session.add(journalist)
                    db.session.flush()
                
                # Parse publication date
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
                    sentiment_score=0.0,  # Default neutral sentiment
                    sentiment_label='neutral'
                )
                
                # Define crypto topics and their related keywords
                topic_keywords = {
                    'Bitcoin': ['bitcoin', 'btc'],
                    'Ethereum': ['ethereum', 'eth'],
                    'DeFi': ['defi', 'decentralized finance'],
                    'NFT': ['nft', 'non-fungible'],
                    'Regulation': ['regulation', 'sec', 'compliance', 'legal'],
                    'Exchanges': ['exchange', 'trading', 'binance', 'coinbase'],
                    'Cryptocurrency': ['cryptocurrency', 'crypto']
                }
                
                # Check article text for topic keywords
                article_text = (article_data.get('title', '') + ' ' + 
                               article_data.get('description', '')).lower()
                
                for topic_name, keywords in topic_keywords.items():
                    if any(keyword.lower() in article_text for keyword in keywords):
                        # Find or create the topic
                        topic = Topic.query.filter_by(name=topic_name).first()
                        if not topic:
                            topic = Topic(name=topic_name)
                            db.session.add(topic)
                            db.session.flush()
                        
                        # Add topic to article
                        article.topics.append(topic)
                
                # Add article to database
                db.session.add(article)
                articles_added += 1
                logger.info(f"Added article: {article.title}")
            
            # Commit all changes at once
            if articles_added > 0:
                db.session.commit()
                logger.info(f"Successfully added {articles_added} articles")
            
            return articles_added
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting to add recent crypto articles")
    result = add_recent_articles()
    
    if result:
        logger.info(f"Added {result} new articles successfully")
    else:
        logger.error("Failed to add recent articles")