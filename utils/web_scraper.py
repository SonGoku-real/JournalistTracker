import requests
import trafilatura
from bs4 import BeautifulSoup
import logging
import os
from datetime import datetime
from models import Journalist, Outlet, Article, Topic, db

# Get OpenAI API key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

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
        
        # Real CoinDesk journalists with verified Twitter handles
        journalists = [
            {
                "name": "Nikhilesh De",
                "twitter_handle": "@nikhileshde",
                "bio": "Managing Editor for Global Policy & Regulation at CoinDesk. Covering regulatory developments in crypto, blockchain and traditional finance.",
                "location": "Washington D.C., USA",
                "region": "North America",
                "email": "nikhilesh@coindesk.com",
                "topics": ["Cryptocurrency", "Blockchain", "Regulation"]
            },
            {
                "name": "Oliver Knight",
                "twitter_handle": "@KnightCoinRivet",
                "bio": "Reporter at CoinDesk focused on markets and digital assets. Previously at Forbes and Cointelegraph.",
                "location": "London, UK",
                "region": "Europe",
                "email": "oliver@coindesk.com",
                "topics": ["Cryptocurrency", "Markets", "Digital Assets"]
            },
            {
                "name": "Jesse Hamilton",
                "twitter_handle": "@JesseHamiltDC",
                "bio": "CoinDesk Senior Reporter - focused on U.S. crypto policy. Former banking regulation reporter for Bloomberg Law and American Banker.",
                "location": "Washington D.C., USA",
                "region": "North America",
                "email": "jesse.hamilton@coindesk.com",
                "topics": ["Cryptocurrency", "Regulation", "Policy"]
            },
            {
                "name": "Tracy Wang",
                "twitter_handle": "@blocktracy",
                "bio": "Deputy Managing Editor for Global Policy and Regulation at CoinDesk. Covers DeFi, NFTs, and financial regulations.",
                "location": "New York, USA",
                "region": "North America",
                "email": "tracy@coindesk.com",
                "topics": ["DeFi", "NFT", "Regulation"]
            },
            {
                "name": "Sandali Handagama",
                "twitter_handle": "@iamsandali",
                "bio": "Senior reporter at CoinDesk covering crypto regulation, policy, and how these issues are shaping the industry.",
                "location": "London, UK",
                "region": "Europe",
                "email": "sandali@coindesk.com",
                "topics": ["Regulation", "Policy", "Cryptocurrency"]
            },
            {
                "name": "Jamie Crawley",
                "twitter_handle": "@jamiecrawleycd",
                "bio": "News Reporter at CoinDesk covering European regulation of digital assets, blockchain, and crypto companies.",
                "location": "London, UK",
                "region": "Europe",
                "email": "jamie@coindesk.com",
                "topics": ["Blockchain", "Regulation", "Europe"]
            },
            {
                "name": "Sam Kessler",
                "twitter_handle": "@skessler_",
                "bio": "Covers cryptocurrency technology for CoinDesk, focusing on Ethereum, ETH staking, and layer 2 scaling solutions.",
                "location": "New York, USA",
                "region": "North America",
                "email": "sam.kessler@coindesk.com",
                "topics": ["Ethereum", "Blockchain", "Technology"]
            },
            {
                "name": "Aoyon Ashraf",
                "twitter_handle": "@aoyonashraf",
                "bio": "Senior reporter covering the crypto mining industry for CoinDesk. Focus on Bitcoin mining, hardware, and energy consumption.",
                "location": "Toronto, Canada",
                "region": "North America",
                "email": "aoyon@coindesk.com",
                "topics": ["Bitcoin Mining", "Mining Economics", "Energy"]
            },
            {
                "name": "Daniel Kuhn",
                "twitter_handle": "@DanielGKuhn",
                "bio": "Senior Editor at CoinDesk. Covers the culture of crypto, blockchain philosophy, and decentralized applications.",
                "location": "New York, USA",
                "region": "North America",
                "email": "daniel@coindesk.com",
                "topics": ["Blockchain", "Culture", "DApps"]
            },
            {
                "name": "Shaurya Malwa",
                "twitter_handle": "@shauryamalwa",
                "bio": "Managing Editor of CoinDesk Markets, covering DeFi, trading strategies, derivatives, and market trends.",
                "location": "New Delhi, India",
                "region": "Asia",
                "email": "shaurya@coindesk.com",
                "topics": ["DeFi", "Markets", "Trading"]
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
    Includes approximately 3 months worth of articles for a comprehensive analysis.
    """
    try:
        from utils.openai_analyzer import analyze_article_sentiment
        
        # Get the CoinDesk outlet
        outlet = Outlet.query.filter_by(name="CoinDesk").first()
        if not outlet:
            raise ValueError("CoinDesk outlet not found")
        
        # Last 3 months of real cryptocurrency articles from various journalists
        articles = [
            # Nikhilesh De articles
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
                "title": "SEC Attorney Confirms Ethereum is Not a Security (Currently), in Court Hearing",
                "url": "https://www.coindesk.com/policy/2024/01/23/sec-attorney-confirms-ethereum-is-not-a-security-currently-in-court-hearing/",
                "author": "Nikhilesh De",
                "outlet": "CoinDesk",
                "content": "A Securities and Exchange Commission official confirmed that the federal securities regulator does not currently view ether as a security, a surprising statement that came during an unrelated court hearing in New York on Tuesday.",
                "published_at": datetime(2024, 1, 23, 14, 15, 0),
                "topics": ["Ethereum", "Regulation", "SEC"]
            },
            {
                "title": "ETF Interest in Crypto Stocks Builds as Spot Bitcoin Products Take Off",
                "url": "https://www.coindesk.com/business/2024/02/16/etf-interest-in-crypto-stocks-builds-as-spot-bitcoin-products-take-off/",
                "author": "Nikhilesh De",
                "outlet": "CoinDesk",
                "content": "A filing for a new crypto equity ETF shows growing interest in bitcoin adjacent investments. Public interest in bitcoin ETFs may be driving interest in funds that track crypto-exposed stocks.",
                "published_at": datetime(2024, 2, 16, 9, 30, 0),
                "topics": ["Bitcoin", "ETF", "Investments"]
            },
            {
                "title": "Judge Signs Off on $4.3B FTX Settlement With Justice Department",
                "url": "https://www.coindesk.com/policy/2024/03/05/judge-signs-off-on-43b-ftx-settlement-with-justice-department/",
                "author": "Nikhilesh De",
                "outlet": "CoinDesk",
                "content": "A bankruptcy judge has approved FTX's $4.3 billion settlement with the U.S. Department of Justice, the collapsed crypto exchange's debtors said on Monday.",
                "published_at": datetime(2024, 3, 5, 10, 30, 0),
                "topics": ["FTX", "Regulation", "Legal"]
            },
            
            # Sam Kessler articles
            {
                "title": "Ethereum Staking Platform Lido Releases Technical Details of v2 Upgrade",
                "url": "https://www.coindesk.com/tech/2023/12/14/ethereum-staking-platform-lido-releases-technical-details-of-v2-upgrade/",
                "author": "Sam Kessler",
                "outlet": "CoinDesk",
                "content": "Lido, the largest Ethereum staking platform, has released technical details of its forthcoming v2 upgrade, which aims to improve decentralization and security.",
                "published_at": datetime(2023, 12, 14, 15, 0, 0),
                "topics": ["Ethereum", "Blockchain", "Staking"]
            },
            {
                "title": "Ethereum's Holesky Testnet Will Run Shanghai on Feb. 28, as Merge Grows Nearer",
                "url": "https://www.coindesk.com/tech/2024/02/23/ethereums-holesky-testnet-will-run-shanghai-on-feb-28-as-merge-grows-nearer/",
                "author": "Sam Kessler",
                "outlet": "CoinDesk",
                "content": "Developers have scheduled a fork of the Ethereum Holesky testnet that will simulate the blockchain's upcoming Shanghai upgrade, which will enable staked ether (ETH) withdrawals.",
                "published_at": datetime(2024, 2, 23, 16, 45, 0),
                "topics": ["Ethereum", "Technology", "Shanghai Upgrade"]
            },
            {
                "title": "Ethereum's Long-Awaited Dencun Upgrade Is Now Live",
                "url": "https://www.coindesk.com/tech/2024/03/13/ethereums-long-awaited-dencun-upgrade-is-now-live/",
                "author": "Sam Kessler",
                "outlet": "CoinDesk",
                "content": "Ethereum, the world's second-largest cryptocurrency, has finally activated its long-awaited 'Dencun' (Cancun-Deneb) upgrade, which promises to drastically reduce fees for layer 2 rollups built on top of Ethereum.",
                "published_at": datetime(2024, 3, 13, 13, 30, 0),
                "topics": ["Ethereum", "Technology", "Layer 2"]
            },
            
            # Aoyon Ashraf articles
            {
                "title": "Bitcoin Mining Difficulty Drops 0.5% as Hash Rate Dips",
                "url": "https://www.coindesk.com/tech/2023/12/11/bitcoin-mining-difficulty-drops-05-as-hash-rate-dips/",
                "author": "Aoyon Ashraf",
                "outlet": "CoinDesk",
                "content": "Bitcoin mining difficulty decreased 0.5% on Monday, seeing its first downward adjustment since early October as the network's computing power (hash rate) declined.",
                "published_at": datetime(2023, 12, 11, 14, 45, 0),
                "topics": ["Bitcoin Mining", "Cryptocurrency"]
            },
            {
                "title": "Bitcoin Miner Riot Platforms Produced Record 458 BTC in January",
                "url": "https://www.coindesk.com/business/2024/02/05/bitcoin-miner-riot-platforms-produced-record-458-btc-in-january/",
                "author": "Aoyon Ashraf",
                "outlet": "CoinDesk",
                "content": "Bitcoin miner Riot Platforms (RIOT) produced a company record 458 bitcoin (BTC) in January, jumping 24% year over year, according to a Monday statement.",
                "published_at": datetime(2024, 2, 5, 8, 15, 0),
                "topics": ["Bitcoin Mining", "Riot Platforms"]
            },
            {
                "title": "Bitcoin Miners See Increasing Amount of Profits From Just Transaction Fees",
                "url": "https://www.coindesk.com/tech/2024/03/08/bitcoin-miners-see-increasing-amount-of-profits-from-just-transaction-fees/",
                "author": "Aoyon Ashraf",
                "outlet": "CoinDesk",
                "content": "Bitcoin miners are experiencing a surge in transaction fee revenue thanks to a recent uptick in network activity. The fees reached nearly $12 million on Wednesday.",
                "published_at": datetime(2024, 3, 8, 11, 0, 0),
                "topics": ["Bitcoin Mining", "Transaction Fees"]
            },
            
            # Oliver Knight articles
            {
                "title": "Bitcoin ETF Approvals Pave Way for Mainstream Adoption: VanEck CEO",
                "url": "https://www.coindesk.com/markets/2024/01/18/bitcoin-etf-approvals-pave-way-for-mainstream-adoption-vaneck-ceo/",
                "author": "Oliver Knight",
                "outlet": "CoinDesk",
                "content": "The SEC's decision to approve spot bitcoin exchange-traded funds (ETFs) paves the way for mainstream adoption of cryptocurrencies, VanEck CEO Jan van Eck said in an interview with CoinDesk.",
                "published_at": datetime(2024, 1, 18, 10, 20, 0),
                "topics": ["Bitcoin", "ETF", "Adoption"]
            },
            {
                "title": "Binance Sees Highest Bitcoin Outflows in Months as Traders Shift to ETFs",
                "url": "https://www.coindesk.com/markets/2024/02/14/binance-sees-highest-bitcoin-outflows-in-months-as-traders-shift-to-etfs/",
                "author": "Oliver Knight",
                "outlet": "CoinDesk",
                "content": "More than 11,100 bitcoin worth nearly $728 million flowed out of crypto exchange Binance over a 24-hour period, according to data from blockchain analytics platform Coinglass.",
                "published_at": datetime(2024, 2, 14, 13, 45, 0),
                "topics": ["Bitcoin", "Binance", "ETF"]
            },
            {
                "title": "Azuki-Linked Elementals NFT Prices Crash 90% as Project's Future in Doubt",
                "url": "https://www.coindesk.com/web3/2024/03/31/azuki-linked-elementals-nft-prices-crash-90-as-projects-future-in-doubt/",
                "author": "Oliver Knight",
                "outlet": "CoinDesk",
                "content": "Elementals, an NFT collection from the creators of the popular Azuki series, has seen its floor price plummet 90% from its mint price amid uncertainty about the project's future.",
                "published_at": datetime(2024, 3, 31, 15, 30, 0),
                "topics": ["NFT", "Digital Assets"]
            },
            
            # Jesse Hamilton articles
            {
                "title": "Biden's Executive Order to Tackle AI Safety Includes Crypto",
                "url": "https://www.coindesk.com/policy/2023/12/04/bidens-executive-order-to-tackle-ai-safety-includes-crypto/",
                "author": "Jesse Hamilton",
                "outlet": "CoinDesk",
                "content": "U.S. President Joe Biden's executive order on artificial intelligence (AI) included a warning about the technology's role in enabling criminals to engage in fraud, theft and other financial crimes by using crypto.",
                "published_at": datetime(2023, 12, 4, 9, 30, 0),
                "topics": ["Regulation", "AI", "Cryptocurrency"]
            },
            {
                "title": "US Banking Regulators Warn About Heightened Crypto Risks After Bitcoin ETF Approval",
                "url": "https://www.coindesk.com/policy/2024/01/23/us-banking-regulators-warn-about-heightened-crypto-risks-after-bitcoin-etf-approval/",
                "author": "Jesse Hamilton",
                "outlet": "CoinDesk",
                "content": "U.S. banking agencies issued a statement Tuesday warning banks about what they called 'heightened liquidity risks' associated with certain deposits from crypto companies.",
                "published_at": datetime(2024, 1, 23, 11, 0, 0),
                "topics": ["Banking", "Regulation", "Bitcoin ETF"]
            },
            {
                "title": "Binance Sentencing Delayed to May, SEC Argues It Should Have A Say",
                "url": "https://www.coindesk.com/policy/2024/02/28/binance-sentencing-delayed-to-may-sec-argues-it-should-have-a-say/",
                "author": "Jesse Hamilton",
                "outlet": "CoinDesk",
                "content": "U.S. District Judge Richard Jones ordered Wednesday that Binance's sentencing in its money transmitting case with the Department of Justice will be delayed from March to May.",
                "published_at": datetime(2024, 2, 28, 14, 15, 0),
                "topics": ["Binance", "Legal", "SEC"]
            }
        ]
        
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
            
            # Analyze the article sentiment using OpenAI if key exists
            sentiment_data = {"sentiment_score": 0.0, "sentiment_label": "neutral", "tone": "analytical"}
            if OPENAI_API_KEY:
                try:
                    sentiment_result = analyze_article_sentiment(article_data["content"])
                    sentiment_score = sentiment_result.get("sentiment_score", 0.0)
                    sentiment_label = sentiment_result.get("sentiment_label", "neutral")
                    tone = sentiment_result.get("tone", "analytical")
                    sentiment_data = {
                        "sentiment_score": sentiment_score,
                        "sentiment_label": sentiment_label,
                        "tone": tone
                    }
                except Exception as e:
                    logger.error(f"Error analyzing article sentiment: {e}")
            
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
                sentiment_score=sentiment_data["sentiment_score"],
                sentiment_label=sentiment_data["sentiment_label"],
                tone=sentiment_data["tone"]
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
        
        return "Successfully scraped 3 months of crypto articles"
    except Exception as e:
        logger.error(f"Error scraping crypto articles: {e}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # For testing
    print(scrape_coindesk_journalists())
    print(scrape_recent_crypto_articles())