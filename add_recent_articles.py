from app import app
from models import Journalist, Outlet, Article, Topic, db
from datetime import datetime

def add_recent_articles():
    """
    Add articles from January-March 2024 to provide 3 months of data for analysis.
    """
    with app.app_context():
        try:
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
            
            # January-March 2024 articles
            recent_articles = [
                # January 2024 - Nikhilesh De
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
                
                # January 2024 - Oliver Knight
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
                
                # January 2024 - Jesse Hamilton
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
                
                # February 2024 - Nikhilesh De
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
                
                # February 2024 - Sam Kessler
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
                
                # February 2024 - Oliver Knight
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
                
                # February 2024 - Jesse Hamilton
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
                },
                
                # February 2024 - Aoyon Ashraf
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
                
                # March 2024 - Nikhilesh De
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
                
                # March 2024 - Sam Kessler
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
                
                # March 2024 - Oliver Knight
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
                
                # March 2024 - Aoyon Ashraf
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
                }
            ]
            
            # Add articles to database
            articles_added = 0
            
            for article_data in recent_articles:
                # Check if article already exists
                existing_article = Article.query.filter_by(url=article_data["url"]).first()
                if existing_article:
                    print(f"Article already exists: {article_data['title']}")
                    continue
                
                # Create new article
                article = Article(
                    title=article_data["title"],
                    url=article_data["url"],
                    content=article_data["content"],
                    published_at=article_data["published_at"],
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    journalist_id=article_data["journalist_id"],
                    outlet_id=article_data["outlet_id"],
                    sentiment_score=article_data["sentiment_score"],
                    sentiment_label=article_data["sentiment_label"]
                )
                
                # Add topics to the article
                for topic in article_data["topics"]:
                    if topic:
                        article.topics.append(topic)
                
                db.session.add(article)
                articles_added += 1
            
            db.session.commit()
            print(f"Successfully added {articles_added} recent articles from Jan-Mar 2024")
            
            return True
        except Exception as e:
            print(f"Error adding recent articles: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    add_recent_articles()