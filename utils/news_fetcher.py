import requests
import logging
import os
from datetime import datetime, timedelta
from app import app
from models import Article, Journalist, Outlet, Topic, db
from utils.openai_analyzer import analyze_article_sentiment, extract_article_topics, summarize_article
from utils.web_scraper import get_website_text_content

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# News API configuration
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

# List of cryptocurrency keywords to track
CRYPTO_KEYWORDS = [
    "bitcoin", "ethereum", "cryptocurrency", "blockchain", "web3",
    "crypto", "defi", "nft", "token", "coinbase", "binance"
]

def fetch_latest_crypto_news(days=1):
    """
    Fetch the latest cryptocurrency news articles using the News API.
    
    Args:
        days (int): Number of days to look back for articles
        
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
        
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        if data.get('status') != 'ok':
            logger.error(f"API returned error: {data.get('message', 'Unknown error')}")
            return []
            
        return data.get('articles', [])
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []

def process_news_articles(articles, analyze_content=True):
    """
    Process news articles and save them to the database.
    
    Args:
        articles (list): List of article dictionaries from the News API
        analyze_content (bool): Whether to analyze the content using OpenAI
        
    Returns:
        int: Number of new articles added
    """
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
            outlet = Outlet.query.filter_by(name=source_name).first()
            if not outlet:
                outlet = Outlet(
                    name=source_name,
                    website=None,  # We don't have the website URL from the API
                    country=None,  # We don't have country info
                    description=f"News source: {source_name}",
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
                updated_at=datetime.utcnow()
            )
            
            # If analyze_content is True and we have OpenAI API key, get more data
            if analyze_content and os.environ.get("OPENAI_API_KEY"):
                try:
                    # Try to get full article content
                    full_content = get_website_text_content(article_data['url'])
                    if full_content:
                        article.content = full_content
                        
                        # Analyze sentiment
                        sentiment_data = analyze_article_sentiment(full_content)
                        if sentiment_data:
                            article.sentiment_score = sentiment_data.get('score', 0)
                            article.sentiment_label = sentiment_data.get('label', 'neutral')
                        
                        # Extract topics
                        topic_names = extract_article_topics(full_content)
                        if topic_names:
                            for topic_name in topic_names:
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
                except Exception as e:
                    logger.error(f"Error analyzing article {article_data['url']}: {e}")
            
            # Add and commit
            db.session.add(article)
            articles_added += 1
        
        if articles_added > 0:
            db.session.commit()
            logger.info(f"Added {articles_added} new articles")
        
        return articles_added

def update_news_feed(days=1, analyze=True):
    """
    Update the news feed with the latest crypto articles.
    
    Args:
        days (int): Number of days to look back
        analyze (bool): Whether to analyze content with OpenAI
        
    Returns:
        int: Number of new articles added
    """
    articles = fetch_latest_crypto_news(days)
    if not articles:
        logger.warning("No articles found or API error occurred")
        return 0
        
    return process_news_articles(articles, analyze)

if __name__ == "__main__":
    # When run directly, update the news feed
    count = update_news_feed()
    print(f"Added {count} new articles to the database")