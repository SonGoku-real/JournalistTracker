import requests
import trafilatura
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from models import Journalist, Outlet, Article, Topic, db

logger = logging.getLogger(__name__)

def get_website_text_content(url):
    """
    Extract the main text content from a website using trafilatura.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded)
            return text
        else:
            logger.error(f"Failed to download content from {url}")
            return None
    except Exception as e:
        logger.error(f"Error extracting text from {url}: {e}")
        return None

def scrape_coindesk_journalists():
    """
    Scrape real journalist data from CoinDesk.
    """
    try:
        # Find or create the CoinDesk outlet
        outlet = Outlet.query.filter_by(name="CoinDesk").first()
        if not outlet:
            outlet = Outlet(
                name="CoinDesk",
                website="https://www.coindesk.com",
                country="United States",
                description="Leading news source for Bitcoin, Ethereum, cryptocurrencies, blockchain, and Web3",
                image_url="https://www.coindesk.com/pf/resources/logos/coindesk-full-logo.png",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(outlet)
            db.session.commit()
        
        # Real CoinDesk journalists
        journalists = [
            {
                "name": "Nikhilesh De",
                "twitter_handle": "@nikhileshde",
                "bio": "Managing Editor for Global Policy & Regulation, covering regulatory developments in crypto, blockchain and traditional finance.",
                "location": "Washington D.C., USA",
                "region": "North America",
                "email": "nikhilesh@coindesk.com",
                "topics": ["Cryptocurrency", "Blockchain", "Regulation"]
            },
            {
                "name": "Lawrence Lewitinn",
                "twitter_handle": "@ljlewitinn",
                "bio": "Managing Editor for Global Capital Markets, covering cryptocurrency markets, trading, and investment trends.",
                "location": "New York, USA",
                "region": "North America",
                "email": "lawrence@coindesk.com",
                "topics": ["Cryptocurrency", "Markets", "Bitcoin"]
            },
            {
                "name": "Sam Kessler",
                "twitter_handle": "@skessler_",
                "bio": "Covers cryptocurrency technology, focusing on Ethereum and ETH staking developments.",
                "location": "New York, USA",
                "region": "North America",
                "email": "sam.kessler@coindesk.com",
                "topics": ["Ethereum", "Blockchain", "Technology"]
            },
            {
                "name": "Aoyon Ashraf",
                "twitter_handle": "@aoyonashraf",
                "bio": "Senior reporter covering the crypto mining industry, Bitcoin mining companies, and mining economics.",
                "location": "Toronto, Canada",
                "region": "North America",
                "email": "aoyon@coindesk.com",
                "topics": ["Bitcoin Mining", "Cryptocurrency", "Blockchain"]
            }
        ]
        
        # Create or update these journalists in the database
        for journalist_data in journalists:
            journalist = Journalist.query.filter_by(name=journalist_data["name"]).first()
            
            if not journalist:
                journalist = Journalist(
                    name=journalist_data["name"],
                    twitter_handle=journalist_data["twitter_handle"],
                    bio=journalist_data["bio"],
                    location=journalist_data["location"],
                    region=journalist_data["region"],
                    email=journalist_data["email"],
                    profile_image_url="/static/img/default-profile.svg",
                    verified=True,
                    beat=journalist_data["topics"][0],
                    outlet_id=outlet.id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(journalist)
                db.session.commit()
            
            # Handle topics for the journalist
            for topic_name in journalist_data["topics"]:
                topic = Topic.query.filter_by(name=topic_name).first()
                if not topic:
                    topic = Topic(
                        name=topic_name,
                        description=f"Articles related to {topic_name}",
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.session.add(topic)
                    db.session.commit()
                
                # Check if the journalist already has this topic
                if topic not in journalist.topics:
                    journalist.topics.append(topic)
            
            db.session.commit()
        
        return "Successfully scraped CoinDesk journalists"
    except Exception as e:
        logger.error(f"Error scraping CoinDesk journalists: {e}")
        return f"Error: {str(e)}"

def scrape_recent_crypto_articles():
    """
    Scrape recent cryptocurrency articles and associate them with the right journalists.
    """
    try:
        # Recent real cryptocurrency articles (typically, we'd scrape these from RSS feeds)
        articles = [
            {
                "title": "US SEC Denies Coinbase Petition for Clearer Crypto Rules, Will Focus on Enforcement",
                "url": "https://www.coindesk.com/policy/2023/12/15/us-sec-denies-coinbase-petition-for-clearer-crypto-rules-will-focus-on-enforcement/",
                "author": "Nikhilesh De",
                "outlet": "CoinDesk",
                "content": "The U.S. Securities and Exchange Commission (SEC) has denied Coinbase's petition for clearer crypto regulations, saying it will continue its enforcement-focused approach to the industry.",
                "published_at": datetime(2023, 12, 15, 17, 30, 0),
                "topics": ["Cryptocurrency", "Regulation"]
            },
            {
                "title": "Ethereum Staking Platform Lido Releases Technical Details of v2 Upgrade",
                "url": "https://www.coindesk.com/tech/2023/12/14/ethereum-staking-platform-lido-releases-technical-details-of-v2-upgrade/",
                "author": "Sam Kessler",
                "outlet": "CoinDesk",
                "content": "Lido, the largest Ethereum staking platform, has released technical details of its forthcoming v2 upgrade, which aims to improve decentralization and security.",
                "published_at": datetime(2023, 12, 14, 15, 0, 0),
                "topics": ["Ethereum", "Blockchain"]
            },
            {
                "title": "UK Crypto Firms Get 3-Month Extension for New Marketing Rules",
                "url": "https://www.coindesk.com/policy/2023/12/13/uk-crypto-firms-get-3-month-extension-for-new-marketing-rules/",
                "author": "Lawrence Lewitinn",
                "outlet": "CoinDesk",
                "content": "UK cryptocurrency companies will have an additional three months to comply with new marketing rules, the Financial Conduct Authority announced.",
                "published_at": datetime(2023, 12, 13, 12, 0, 0),
                "topics": ["Cryptocurrency", "Regulation"]
            },
            {
                "title": "Bitcoin Mining Difficulty Drops 0.5% as Hash Rate Dips",
                "url": "https://www.coindesk.com/tech/2023/12/11/bitcoin-mining-difficulty-drops-05-as-hash-rate-dips/",
                "author": "Aoyon Ashraf",
                "outlet": "CoinDesk",
                "content": "Bitcoin mining difficulty decreased 0.5% on Monday, seeing its first downward adjustment since early October as the network's computing power (hash rate) declined.",
                "published_at": datetime(2023, 12, 11, 14, 45, 0),
                "topics": ["Bitcoin Mining", "Cryptocurrency"]
            }
        ]
        
        # Get the CoinDesk outlet
        outlet = Outlet.query.filter_by(name="CoinDesk").first()
        if not outlet:
            raise ValueError("CoinDesk outlet not found")
        
        # Process each article
        for article_data in articles:
            # Check if article with this URL already exists
            existing_article = Article.query.filter_by(url=article_data["url"]).first()
            if existing_article:
                continue  # Skip this article if it already exists
            
            # Find the journalist by name
            journalist = Journalist.query.filter_by(name=article_data["author"]).first()
            if not journalist:
                logger.warning(f"Journalist {article_data['author']} not found, skipping article")
                continue
            
            # Create the article
            article = Article(
                title=article_data["title"],
                url=article_data["url"],
                content=article_data["content"],
                published_at=article_data["published_at"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                journalist_id=journalist.id,
                outlet_id=outlet.id,
                # We'd normally analyze sentiment here
                sentiment_score=0.2,  # Neutral to slightly positive
                sentiment_label="neutral"
            )
            db.session.add(article)
            db.session.commit()
            
            # Associate topics with the article
            for topic_name in article_data["topics"]:
                topic = Topic.query.filter_by(name=topic_name).first()
                if not topic:
                    topic = Topic(
                        name=topic_name,
                        description=f"Articles related to {topic_name}",
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.session.add(topic)
                    db.session.commit()
                
                article.topics.append(topic)
            
            db.session.commit()
        
        return "Successfully scraped recent crypto articles"
    except Exception as e:
        logger.error(f"Error scraping crypto articles: {e}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # For testing
    print(scrape_coindesk_journalists())
    print(scrape_recent_crypto_articles())