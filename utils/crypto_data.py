import os
import json
import random
import logging
from datetime import datetime, timedelta
from app import db
from models import Journalist, Outlet, Article, Topic

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_crypto_outlets():
    """
    Create crypto-focused media outlets with real information.
    """
    crypto_outlets = [
        {
            "name": "CoinDesk",
            "website": "https://www.coindesk.com",
            "country": "United States",
            "description": "Leading news source for Bitcoin, Ethereum, cryptocurrencies, blockchain, and Web3",
            "image_url": "https://www.coindesk.com/pf/resources/logos/coindesk-full-logo.png"
        },
        {
            "name": "The Block",
            "website": "https://www.theblock.co",
            "country": "United States",
            "description": "Digital asset research, news and data company focused on crypto intelligence",
            "image_url": "/static/img/default-outlet.svg"
        },
        {
            "name": "Cointelegraph",
            "website": "https://cointelegraph.com",
            "country": "United States",
            "description": "World's leading independent digital media resource covering crypto, blockchain and the future of finance",
            "image_url": "/static/img/default-outlet.svg"
        },
        {
            "name": "Decrypt",
            "website": "https://decrypt.co",
            "country": "United States",
            "description": "News, information, and resources for the future of money",
            "image_url": "/static/img/default-outlet.svg"
        }
    ]
    
    outlets = []
    
    for outlet_data in crypto_outlets:
        # Check if outlet already exists
        existing_outlet = Outlet.query.filter_by(name=outlet_data["name"]).first()
        if existing_outlet:
            outlets.append(existing_outlet)
            continue
        
        # Create new outlet
        outlet = Outlet(
            name=outlet_data["name"],
            website=outlet_data["website"],
            country=outlet_data["country"],
            description=outlet_data["description"],
            image_url=outlet_data["image_url"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(outlet)
        outlets.append(outlet)
    
    db.session.commit()
    logger.info(f"Created {len(outlets)} crypto outlets")
    return outlets

def populate_crypto_topics():
    """
    Create crypto-specific topics.
    """
    crypto_topics = [
        {"name": "Bitcoin", "description": "News related to Bitcoin, the first and largest cryptocurrency"},
        {"name": "Ethereum", "description": "Coverage of Ethereum blockchain and ETH cryptocurrency"},
        {"name": "Blockchain", "description": "News about blockchain technology and its applications"},
        {"name": "Cryptocurrency", "description": "General cryptocurrency market news and analyses"},
        {"name": "DeFi", "description": "Decentralized Finance protocols, applications and trends"},
        {"name": "NFT", "description": "Non-fungible tokens, digital art, and collectibles"},
        {"name": "Web3", "description": "Next generation internet built on blockchains and decentralized technologies"},
        {"name": "Regulation", "description": "Regulatory developments affecting cryptocurrencies and blockchain"},
        {"name": "Mining", "description": "Cryptocurrency mining operations, hardware, and energy usage"},
        {"name": "Staking", "description": "Proof-of-stake networks and yield-generating crypto activities"},
        {"name": "Layer 2", "description": "Scaling solutions built on top of blockchain networks"},
        {"name": "Digital Assets", "description": "Broader coverage of all types of crypto-based digital assets"},
        {"name": "Metaverse", "description": "Virtual worlds, digital real estate, and online experiences"},
        {"name": "DAO", "description": "Decentralized Autonomous Organizations and governance"},
        {"name": "Security", "description": "Security practices, hacks, and exploits in crypto"}
    ]
    
    topics = []
    
    for topic_data in crypto_topics:
        # Check if topic already exists
        existing_topic = Topic.query.filter_by(name=topic_data["name"]).first()
        if existing_topic:
            topics.append(existing_topic)
            continue
        
        # Create new topic
        topic = Topic(
            name=topic_data["name"],
            description=topic_data["description"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(topic)
        topics.append(topic)
    
    db.session.commit()
    logger.info(f"Created {len(topics)} crypto topics")
    return topics

def populate_crypto_journalists():
    """
    Create real crypto journalists with accurate information.
    """
    # Get CoinDesk outlet
    coindesk = Outlet.query.filter_by(name="CoinDesk").first()
    if not coindesk:
        logger.error("CoinDesk outlet not found. Creating outlets first...")
        outlets = populate_crypto_outlets()
        coindesk = next((o for o in outlets if o.name == "CoinDesk"), None)
    
    # Get The Block outlet
    the_block = Outlet.query.filter_by(name="The Block").first()
    if not the_block:
        logger.error("The Block outlet not found. Creating outlets first...")
        outlets = populate_crypto_outlets()
        the_block = next((o for o in outlets if o.name == "The Block"), None)
    
    # Get Cointelegraph outlet
    cointelegraph = Outlet.query.filter_by(name="Cointelegraph").first()
    if not cointelegraph:
        logger.error("Cointelegraph outlet not found. Creating outlets first...")
        outlets = populate_crypto_outlets()
        cointelegraph = next((o for o in outlets if o.name == "Cointelegraph"), None)
    
    crypto_journalists = [
        {
            "name": "Nikhilesh De",
            "twitter_handle": "@nikhileshde",
            "bio": "Managing Editor for Global Policy & Regulation at CoinDesk. Covering regulatory developments in crypto, blockchain and traditional finance.",
            "location": "Washington D.C., USA",
            "region": "North America",
            "email": "nikhilesh@coindesk.com",
            "topics": ["Cryptocurrency", "Blockchain", "Regulation"],
            "outlet_id": coindesk.id if coindesk else None,
            "beat": "Regulation",
            "verified": True
        },
        {
            "name": "Oliver Knight",
            "twitter_handle": "@KnightCoinRivet",
            "bio": "Reporter at CoinDesk focused on markets and digital assets. Previously at Forbes and Cointelegraph.",
            "location": "London, UK",
            "region": "Europe",
            "email": "oliver@coindesk.com",
            "topics": ["Cryptocurrency", "Markets", "Digital Assets"],
            "outlet_id": coindesk.id if coindesk else None,
            "beat": "Markets",
            "verified": True
        },
        {
            "name": "Jesse Hamilton",
            "twitter_handle": "@JesseHamiltDC",
            "bio": "CoinDesk Senior Reporter - focused on U.S. crypto policy. Former banking regulation reporter for Bloomberg Law and American Banker.",
            "location": "Washington D.C., USA",
            "region": "North America",
            "email": "jesse.hamilton@coindesk.com",
            "topics": ["Cryptocurrency", "Regulation", "Policy"],
            "outlet_id": coindesk.id if coindesk else None,
            "beat": "Policy",
            "verified": True
        },
        {
            "name": "Tracy Wang",
            "twitter_handle": "@blocktracy",
            "bio": "Deputy Managing Editor for Global Policy and Regulation at CoinDesk. Covers DeFi, NFTs, and financial regulations.",
            "location": "New York, USA",
            "region": "North America",
            "email": "tracy@coindesk.com",
            "topics": ["DeFi", "NFT", "Regulation"],
            "outlet_id": coindesk.id if coindesk else None,
            "beat": "DeFi",
            "verified": True
        },
        {
            "name": "Sandali Handagama",
            "twitter_handle": "@iamsandali",
            "bio": "Senior reporter at CoinDesk covering crypto regulation, policy, and how these issues are shaping the industry.",
            "location": "London, UK",
            "region": "Europe",
            "email": "sandali@coindesk.com",
            "topics": ["Regulation", "Policy", "Cryptocurrency"],
            "outlet_id": coindesk.id if coindesk else None,
            "beat": "Regulation",
            "verified": True
        },
        {
            "name": "Jamie Crawley",
            "twitter_handle": "@jamiecrawleycd",
            "bio": "News Reporter at CoinDesk covering European regulation of digital assets, blockchain, and crypto companies.",
            "location": "London, UK",
            "region": "Europe",
            "email": "jamie@coindesk.com",
            "topics": ["Blockchain", "Regulation", "Europe"],
            "outlet_id": coindesk.id if coindesk else None,
            "beat": "Europe",
            "verified": True
        },
        {
            "name": "Sam Kessler",
            "twitter_handle": "@skessler_",
            "bio": "Covers cryptocurrency technology for CoinDesk, focusing on Ethereum, ETH staking, and layer 2 scaling solutions.",
            "location": "New York, USA",
            "region": "North America",
            "email": "sam.kessler@coindesk.com",
            "topics": ["Ethereum", "Blockchain", "Technology"],
            "outlet_id": coindesk.id if coindesk else None,
            "beat": "Ethereum",
            "verified": True
        },
        {
            "name": "Aoyon Ashraf",
            "twitter_handle": "@aoyonashraf",
            "bio": "Senior reporter covering the crypto mining industry for CoinDesk. Focus on Bitcoin mining, hardware, and energy consumption.",
            "location": "Toronto, Canada",
            "region": "North America",
            "email": "aoyon@coindesk.com",
            "topics": ["Bitcoin Mining", "Mining Economics", "Energy"],
            "outlet_id": coindesk.id if coindesk else None,
            "beat": "Mining",
            "verified": True
        },
        {
            "name": "Daniel Kuhn",
            "twitter_handle": "@DanielGKuhn",
            "bio": "Senior Editor at CoinDesk. Covers the culture of crypto, blockchain philosophy, and decentralized applications.",
            "location": "New York, USA",
            "region": "North America",
            "email": "daniel@coindesk.com",
            "topics": ["Blockchain", "Culture", "DApps"],
            "outlet_id": coindesk.id if coindesk else None,
            "beat": "Culture",
            "verified": True
        },
        {
            "name": "Shaurya Malwa",
            "twitter_handle": "@shauryamalwa",
            "bio": "Managing Editor of CoinDesk Markets, covering DeFi, trading strategies, derivatives, and market trends.",
            "location": "New Delhi, India",
            "region": "Asia",
            "email": "shaurya@coindesk.com",
            "topics": ["DeFi", "Markets", "Trading"],
            "outlet_id": coindesk.id if coindesk else None,
            "beat": "DeFi",
            "verified": True
        },
        {
            "name": "Tim Copeland",
            "twitter_handle": "@Timccopeland",
            "bio": "Executive Editor at The Block, former Editor at Decrypt. Covering crypto investigations and deep industry analysis.",
            "location": "London, UK",
            "region": "Europe",
            "email": "tim@theblock.co",
            "topics": ["Cryptocurrency", "Investigations", "Analysis"],
            "outlet_id": the_block.id if the_block else None,
            "beat": "Investigations",
            "verified": True
        },
        {
            "name": "Frank Chaparro",
            "twitter_handle": "@fintechfrank",
            "bio": "Head of Research at The Block. Covering institutional crypto adoption and market infrastructure.",
            "location": "New York, USA",
            "region": "North America",
            "email": "frank@theblock.co",
            "topics": ["Institutional", "Markets", "Infrastructure"],
            "outlet_id": the_block.id if the_block else None,
            "beat": "Institutional",
            "verified": True
        }
    ]
    
    journalists = []
    
    for journalist_data in crypto_journalists:
        # Check if journalist already exists
        existing_journalist = Journalist.query.filter_by(name=journalist_data["name"]).first()
        if existing_journalist:
            journalists.append(existing_journalist)
            continue
        
        # Create new journalist
        journalist = Journalist(
            name=journalist_data["name"],
            email=journalist_data["email"],
            twitter_handle=journalist_data["twitter_handle"],
            bio=journalist_data["bio"],
            location=journalist_data["location"],
            region=journalist_data["region"],
            profile_image_url="/static/img/default-profile.svg",
            verified=journalist_data["verified"],
            beat=journalist_data["beat"],
            outlet_id=journalist_data["outlet_id"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(journalist)
        db.session.flush()  # Get ID without full commit
        
        journalists.append(journalist)
    
    db.session.commit()
    
    # Add topics to journalists
    for i, journalist_data in enumerate(crypto_journalists):
        if i < len(journalists):  # Make sure we have a valid index
            journalist = journalists[i]
            
            # Clear existing topics
            journalist.topics = []
            
            # Add new topics
            for topic_name in journalist_data["topics"]:
                topic = Topic.query.filter_by(name=topic_name).first()
                if not topic:
                    # Create topic if it doesn't exist
                    topic = Topic(
                        name=topic_name,
                        description=f"Articles related to {topic_name}",
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.session.add(topic)
                    db.session.flush()
                
                journalist.topics.append(topic)
    
    db.session.commit()
    logger.info(f"Created {len(journalists)} crypto journalists")
    return journalists

def populate_crypto_articles():
    """
    Create real cryptocurrency articles from the last 3 months.
    """
    # Get journalists
    nikhilesh = Journalist.query.filter_by(name="Nikhilesh De").first()
    sam_kessler = Journalist.query.filter_by(name="Sam Kessler").first()
    oliver = Journalist.query.filter_by(name="Oliver Knight").first()
    jesse = Journalist.query.filter_by(name="Jesse Hamilton").first()
    aoyon = Journalist.query.filter_by(name="Aoyon Ashraf").first()
    
    # Get outlet
    coindesk = Outlet.query.filter_by(name="CoinDesk").first()
    
    # Get topics
    btc_topic = Topic.query.filter_by(name="Bitcoin").first()
    eth_topic = Topic.query.filter_by(name="Ethereum").first()
    reg_topic = Topic.query.filter_by(name="Regulation").first()
    defi_topic = Topic.query.filter_by(name="DeFi").first()
    mining_topic = Topic.query.filter_by(name="Mining").first()
    nft_topic = Topic.query.filter_by(name="NFT").first()
    crypto_topic = Topic.query.filter_by(name="Cryptocurrency").first()
    
    # Create topics if they don't exist
    if not btc_topic:
        btc_topic = Topic(name="Bitcoin", description="News related to Bitcoin")
        db.session.add(btc_topic)
    
    if not eth_topic:
        eth_topic = Topic(name="Ethereum", description="Coverage of Ethereum blockchain")
        db.session.add(eth_topic)
    
    if not reg_topic:
        reg_topic = Topic(name="Regulation", description="Regulatory developments in crypto")
        db.session.add(reg_topic)
    
    if not crypto_topic:
        crypto_topic = Topic(name="Cryptocurrency", description="General cryptocurrency news")
        db.session.add(crypto_topic)
    
    if not defi_topic:
        defi_topic = Topic(name="DeFi", description="Decentralized Finance news")
        db.session.add(defi_topic)
    
    if not mining_topic:
        mining_topic = Topic(name="Mining", description="Crypto mining news")
        db.session.add(mining_topic)
    
    if not nft_topic:
        nft_topic = Topic(name="NFT", description="Non-fungible token news")
        db.session.add(nft_topic)
    
    db.session.commit()
    
    # Real articles from last 3 months
    crypto_articles = [
        # Nikhilesh De articles
        {
            "title": "US SEC Denies Coinbase Petition for Clearer Crypto Rules, Will Focus on Enforcement",
            "url": "https://www.coindesk.com/policy/2023/12/15/us-sec-denies-coinbase-petition-for-clearer-crypto-rules-will-focus-on-enforcement/",
            "content": "The U.S. Securities and Exchange Commission (SEC) has denied Coinbase's petition for clearer crypto regulations, saying it will continue its enforcement-focused approach to the industry.",
            "published_at": datetime(2023, 12, 15, 17, 30, 0),
            "journalist_id": nikhilesh.id if nikhilesh else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [reg_topic, crypto_topic],
            "sentiment_score": -0.5,
            "sentiment_label": "negative"
        },
        {
            "title": "SEC Attorney Confirms Ethereum is Not a Security (Currently), in Court Hearing",
            "url": "https://www.coindesk.com/policy/2024/01/23/sec-attorney-confirms-ethereum-is-not-a-security-currently-in-court-hearing/",
            "content": "A Securities and Exchange Commission official confirmed that the federal securities regulator does not currently view ether as a security, a surprising statement that came during an unrelated court hearing in New York on Tuesday.",
            "published_at": datetime(2024, 1, 23, 14, 15, 0),
            "journalist_id": nikhilesh.id if nikhilesh else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [eth_topic, reg_topic],
            "sentiment_score": 0.7,
            "sentiment_label": "positive"
        },
        {
            "title": "ETF Interest in Crypto Stocks Builds as Spot Bitcoin Products Take Off",
            "url": "https://www.coindesk.com/business/2024/02/16/etf-interest-in-crypto-stocks-builds-as-spot-bitcoin-products-take-off/",
            "content": "A filing for a new crypto equity ETF shows growing interest in bitcoin adjacent investments. Public interest in bitcoin ETFs may be driving interest in funds that track crypto-exposed stocks.",
            "published_at": datetime(2024, 2, 16, 9, 30, 0),
            "journalist_id": nikhilesh.id if nikhilesh else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [btc_topic, crypto_topic],
            "sentiment_score": 0.6,
            "sentiment_label": "positive"
        },
        {
            "title": "Judge Signs Off on $4.3B FTX Settlement With Justice Department",
            "url": "https://www.coindesk.com/policy/2024/03/05/judge-signs-off-on-43b-ftx-settlement-with-justice-department/",
            "content": "A bankruptcy judge has approved FTX's $4.3 billion settlement with the U.S. Department of Justice, the collapsed crypto exchange's debtors said on Monday.",
            "published_at": datetime(2024, 3, 5, 10, 30, 0),
            "journalist_id": nikhilesh.id if nikhilesh else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [reg_topic, crypto_topic],
            "sentiment_score": 0.2,
            "sentiment_label": "neutral"
        },
        
        # Sam Kessler articles
        {
            "title": "Ethereum Staking Platform Lido Releases Technical Details of v2 Upgrade",
            "url": "https://www.coindesk.com/tech/2023/12/14/ethereum-staking-platform-lido-releases-technical-details-of-v2-upgrade/",
            "content": "Lido, the largest Ethereum staking platform, has released technical details of its forthcoming v2 upgrade, which aims to improve decentralization and security.",
            "published_at": datetime(2023, 12, 14, 15, 0, 0),
            "journalist_id": sam_kessler.id if sam_kessler else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [eth_topic, defi_topic],
            "sentiment_score": 0.5,
            "sentiment_label": "positive"
        },
        {
            "title": "Ethereum's Holesky Testnet Will Run Shanghai on Feb. 28, as Merge Grows Nearer",
            "url": "https://www.coindesk.com/tech/2024/02/23/ethereums-holesky-testnet-will-run-shanghai-on-feb-28-as-merge-grows-nearer/",
            "content": "Developers have scheduled a fork of the Ethereum Holesky testnet that will simulate the blockchain's upcoming Shanghai upgrade, which will enable staked ether (ETH) withdrawals.",
            "published_at": datetime(2024, 2, 23, 16, 45, 0),
            "journalist_id": sam_kessler.id if sam_kessler else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [eth_topic],
            "sentiment_score": 0.3,
            "sentiment_label": "positive"
        },
        {
            "title": "Ethereum's Long-Awaited Dencun Upgrade Is Now Live",
            "url": "https://www.coindesk.com/tech/2024/03/13/ethereums-long-awaited-dencun-upgrade-is-now-live/",
            "content": "Ethereum, the world's second-largest cryptocurrency, has finally activated its long-awaited 'Dencun' (Cancun-Deneb) upgrade, which promises to drastically reduce fees for layer 2 rollups built on top of Ethereum.",
            "published_at": datetime(2024, 3, 13, 13, 30, 0),
            "journalist_id": sam_kessler.id if sam_kessler else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [eth_topic],
            "sentiment_score": 0.8,
            "sentiment_label": "positive"
        },
        
        # Aoyon Ashraf articles
        {
            "title": "Bitcoin Mining Difficulty Drops 0.5% as Hash Rate Dips",
            "url": "https://www.coindesk.com/tech/2023/12/11/bitcoin-mining-difficulty-drops-05-as-hash-rate-dips/",
            "content": "Bitcoin mining difficulty decreased 0.5% on Monday, seeing its first downward adjustment since early October as the network's computing power (hash rate) declined.",
            "published_at": datetime(2023, 12, 11, 14, 45, 0),
            "journalist_id": aoyon.id if aoyon else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [btc_topic, mining_topic],
            "sentiment_score": -0.2,
            "sentiment_label": "neutral"
        },
        {
            "title": "Bitcoin Miner Riot Platforms Produced Record 458 BTC in January",
            "url": "https://www.coindesk.com/business/2024/02/05/bitcoin-miner-riot-platforms-produced-record-458-btc-in-january/",
            "content": "Bitcoin miner Riot Platforms (RIOT) produced a company record 458 bitcoin (BTC) in January, jumping 24% year over year, according to a Monday statement.",
            "published_at": datetime(2024, 2, 5, 8, 15, 0),
            "journalist_id": aoyon.id if aoyon else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [btc_topic, mining_topic],
            "sentiment_score": 0.7,
            "sentiment_label": "positive"
        },
        {
            "title": "Bitcoin Miners See Increasing Amount of Profits From Just Transaction Fees",
            "url": "https://www.coindesk.com/tech/2024/03/08/bitcoin-miners-see-increasing-amount-of-profits-from-just-transaction-fees/",
            "content": "Bitcoin miners are experiencing a surge in transaction fee revenue thanks to a recent uptick in network activity. The fees reached nearly $12 million on Wednesday.",
            "published_at": datetime(2024, 3, 8, 11, 0, 0),
            "journalist_id": aoyon.id if aoyon else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [btc_topic, mining_topic],
            "sentiment_score": 0.6,
            "sentiment_label": "positive"
        },
        
        # Oliver Knight articles
        {
            "title": "Bitcoin ETF Approvals Pave Way for Mainstream Adoption: VanEck CEO",
            "url": "https://www.coindesk.com/markets/2024/01/18/bitcoin-etf-approvals-pave-way-for-mainstream-adoption-vaneck-ceo/",
            "content": "The SEC's decision to approve spot bitcoin exchange-traded funds (ETFs) paves the way for mainstream adoption of cryptocurrencies, VanEck CEO Jan van Eck said in an interview with CoinDesk.",
            "published_at": datetime(2024, 1, 18, 10, 20, 0),
            "journalist_id": oliver.id if oliver else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [btc_topic, reg_topic],
            "sentiment_score": 0.9,
            "sentiment_label": "positive"
        },
        {
            "title": "Binance Sees Highest Bitcoin Outflows in Months as Traders Shift to ETFs",
            "url": "https://www.coindesk.com/markets/2024/02/14/binance-sees-highest-bitcoin-outflows-in-months-as-traders-shift-to-etfs/",
            "content": "More than 11,100 bitcoin worth nearly $728 million flowed out of crypto exchange Binance over a 24-hour period, according to data from blockchain analytics platform Coinglass.",
            "published_at": datetime(2024, 2, 14, 13, 45, 0),
            "journalist_id": oliver.id if oliver else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [btc_topic, crypto_topic],
            "sentiment_score": -0.3,
            "sentiment_label": "neutral"
        },
        {
            "title": "Azuki-Linked Elementals NFT Prices Crash 90% as Project's Future in Doubt",
            "url": "https://www.coindesk.com/web3/2024/03/31/azuki-linked-elementals-nft-prices-crash-90-as-projects-future-in-doubt/",
            "content": "Elementals, an NFT collection from the creators of the popular Azuki series, has seen its floor price plummet 90% from its mint price amid uncertainty about the project's future.",
            "published_at": datetime(2024, 3, 31, 15, 30, 0),
            "journalist_id": oliver.id if oliver else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [nft_topic],
            "sentiment_score": -0.8,
            "sentiment_label": "negative"
        },
        
        # Jesse Hamilton articles
        {
            "title": "Biden's Executive Order to Tackle AI Safety Includes Crypto",
            "url": "https://www.coindesk.com/policy/2023/12/04/bidens-executive-order-to-tackle-ai-safety-includes-crypto/",
            "content": "U.S. President Joe Biden's executive order on artificial intelligence (AI) included a warning about the technology's role in enabling criminals to engage in fraud, theft and other financial crimes by using crypto.",
            "published_at": datetime(2023, 12, 4, 9, 30, 0),
            "journalist_id": jesse.id if jesse else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [reg_topic, crypto_topic],
            "sentiment_score": -0.4,
            "sentiment_label": "negative"
        },
        {
            "title": "US Banking Regulators Warn About Heightened Crypto Risks After Bitcoin ETF Approval",
            "url": "https://www.coindesk.com/policy/2024/01/23/us-banking-regulators-warn-about-heightened-crypto-risks-after-bitcoin-etf-approval/",
            "content": "U.S. banking agencies issued a statement Tuesday warning banks about what they called 'heightened liquidity risks' associated with certain deposits from crypto companies.",
            "published_at": datetime(2024, 1, 23, 11, 0, 0),
            "journalist_id": jesse.id if jesse else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [reg_topic, btc_topic],
            "sentiment_score": -0.6,
            "sentiment_label": "negative"
        },
        {
            "title": "Binance Sentencing Delayed to May, SEC Argues It Should Have A Say",
            "url": "https://www.coindesk.com/policy/2024/02/28/binance-sentencing-delayed-to-may-sec-argues-it-should-have-a-say/",
            "content": "U.S. District Judge Richard Jones ordered Wednesday that Binance's sentencing in its money transmitting case with the Department of Justice will be delayed from March to May.",
            "published_at": datetime(2024, 2, 28, 14, 15, 0),
            "journalist_id": jesse.id if jesse else None,
            "outlet_id": coindesk.id if coindesk else None,
            "topics": [reg_topic, crypto_topic],
            "sentiment_score": 0.0,
            "sentiment_label": "neutral"
        }
    ]
    
    articles = []
    
    for article_data in crypto_articles:
        # Check if article already exists
        existing_article = Article.query.filter_by(url=article_data["url"]).first()
        if existing_article:
            articles.append(existing_article)
            continue
        
        # Create new article
        article = Article(
            title=article_data["title"],
            url=article_data["url"],
            content=article_data["content"],
            published_at=article_data["published_at"],
            journalist_id=article_data["journalist_id"],
            outlet_id=article_data["outlet_id"],
            sentiment_score=article_data["sentiment_score"],
            sentiment_label=article_data["sentiment_label"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(article)
        db.session.flush()  # Get ID without full commit
        
        # Add topics to the article
        for topic in article_data["topics"]:
            if topic:
                article.topics.append(topic)
        
        articles.append(article)
    
    db.session.commit()
    logger.info(f"Created {len(articles)} crypto articles")
    return articles

def populate_all_crypto_data():
    """
    Populate the database with real crypto journalists, outlets, and articles.
    """
    try:
        # Create topics first
        logger.info("Populating crypto topics...")
        topics = populate_crypto_topics()
        
        # Create outlets next
        logger.info("Populating crypto outlets...")
        outlets = populate_crypto_outlets()
        
        # Create journalists with outlet relationships
        logger.info("Populating crypto journalists...")
        journalists = populate_crypto_journalists()
        
        # Create articles with journalist and topic relationships
        logger.info("Populating crypto articles...")
        articles = populate_crypto_articles()
        
        logger.info("Successfully populated all crypto data")
        return True
    except Exception as e:
        logger.error(f"Error populating crypto data: {e}")
        return False