from app import app
from models import Journalist, Outlet, Article, Topic, db
from datetime import datetime

def add_block_articles():
    """
    Add articles from The Block journalists (January-March 2024)
    """
    with app.app_context():
        try:
            # Get journalists
            frank = Journalist.query.filter_by(name="Frank Chaparro").first()
            tim = Journalist.query.filter_by(name="Tim Copeland").first()
            michael = Journalist.query.filter_by(name="Michael Rodriguez").first()
            
            # Get outlet
            the_block = Outlet.query.filter_by(name="The Block").first()
            
            # Get topics
            btc_topic = Topic.query.filter_by(name="Bitcoin").first()
            eth_topic = Topic.query.filter_by(name="Ethereum").first()
            reg_topic = Topic.query.filter_by(name="Regulation").first()
            defi_topic = Topic.query.filter_by(name="DeFi").first()
            exchange_topic = Topic.query.filter_by(name="Exchanges").first()
            crypto_topic = Topic.query.filter_by(name="Cryptocurrency").first()
            venture_topic = Topic.query.filter_by(name="Venture Capital").first()
            
            # The Block articles Jan-Mar 2024
            block_articles = [
                # Frank Chaparro
                {
                    "title": "Exclusive: Tiger Global slashing crypto exposure by half, moving away from tokens",
                    "url": "https://www.theblock.co/post/249882/tiger-global-slashing-crypto-exposure-by-half-moving-away-from-tokens",
                    "content": "Tiger Global, one of the most influential investment firms in tech and crypto, is slashing its exposure to digital asset firms as it looks to refocus on traditional equity investments.",
                    "published_at": datetime(2024, 1, 17, 14, 0, 0),
                    "journalist_id": frank.id if frank else None,
                    "outlet_id": the_block.id if the_block else None,
                    "topics": [crypto_topic, venture_topic],
                    "sentiment_score": -0.3,
                    "sentiment_label": "negative"
                },
                {
                    "title": "Cathie Wood's Ark Invest bought nearly $18 million of Coinbase stock last week",
                    "url": "https://www.theblock.co/post/265177/ark-invest-buys-coinbase-stock",
                    "content": "Cathie Wood's Ark Invest scooped up about $18 million worth of Coinbase shares last week as the stock price of the crypto exchange operator surged.",
                    "published_at": datetime(2024, 2, 26, 9, 45, 0),
                    "journalist_id": frank.id if frank else None,
                    "outlet_id": the_block.id if the_block else None,
                    "topics": [exchange_topic, crypto_topic],
                    "sentiment_score": 0.6,
                    "sentiment_label": "positive"
                },
                {
                    "title": "Bitcoin ETFs rake in another $400 million as the token trades sideways",
                    "url": "https://www.theblock.co/post/278038/bitcoin-etfs-rake-in-another-400-million-as-the-token-trades-sideways",
                    "content": "Bitcoin exchange-traded funds saw another strong day of inflows on Monday, even as the price of the leading token by market cap traded sideways.",
                    "published_at": datetime(2024, 3, 26, 10, 30, 0),
                    "journalist_id": frank.id if frank else None,
                    "outlet_id": the_block.id if the_block else None,
                    "topics": [btc_topic, crypto_topic],
                    "sentiment_score": 0.4,
                    "sentiment_label": "positive"
                },
                
                # Tim Copeland
                {
                    "title": "Ethereum developers prepare for next upgrade with shadow fork named Pectra",
                    "url": "https://www.theblock.co/post/253567/ethereum-developers-prepare-for-next-upgrade-with-shadow-fork-named-pectra",
                    "content": "Ethereum developers are testing improvements to the network through a shadow fork named Pectra, ahead of the mainnet's next big upgrade.",
                    "published_at": datetime(2024, 1, 10, 15, 15, 0),
                    "journalist_id": tim.id if tim else None,
                    "outlet_id": the_block.id if the_block else None,
                    "topics": [eth_topic],
                    "sentiment_score": 0.5,
                    "sentiment_label": "positive"
                },
                {
                    "title": "Uniswap community votes to deploy V3 to blockchain Base",
                    "url": "https://www.theblock.co/post/264319/uniswap-community-votes-to-deploy-v3-to-blockchain-base",
                    "content": "Uniswap's community has voted to deploy V3 of its protocol to the Base blockchain, bringing the decentralized exchange to Coinbase's layer-2 network.",
                    "published_at": datetime(2024, 2, 21, 11, 0, 0),
                    "journalist_id": tim.id if tim else None,
                    "outlet_id": the_block.id if the_block else None,
                    "topics": [defi_topic, eth_topic],
                    "sentiment_score": 0.7,
                    "sentiment_label": "positive"
                },
                {
                    "title": "Ethereum upgrade expected early Wednesday morning",
                    "url": "https://www.theblock.co/post/272867/ethereum-upgrade-expected-early-wednesday-morning",
                    "content": "Ethereum's long-awaited Dencun upgrade is expected to activate in the early hours of Wednesday, bringing with it several improvements to the network.",
                    "published_at": datetime(2024, 3, 12, 16, 20, 0),
                    "journalist_id": tim.id if tim else None,
                    "outlet_id": the_block.id if the_block else None,
                    "topics": [eth_topic],
                    "sentiment_score": 0.6,
                    "sentiment_label": "positive"
                },
                
                # Michael Rodriguez
                {
                    "title": "Galaxy Digital applies for Bitcoin ETF in Hong Kong",
                    "url": "https://www.theblock.co/post/256542/galaxy-digital-applies-for-bitcoin-etf-in-hong-kong",
                    "content": "Galaxy Digital has formally applied to offer a Bitcoin exchange-traded fund in Hong Kong, becoming the latest firm looking to expand Bitcoin ETF offerings globally.",
                    "published_at": datetime(2024, 1, 29, 13, 0, 0),
                    "journalist_id": michael.id if michael else None,
                    "outlet_id": the_block.id if the_block else None,
                    "topics": [btc_topic, reg_topic],
                    "sentiment_score": 0.5,
                    "sentiment_label": "positive"
                },
                {
                    "title": "Celsius Network to close operations by end of February",
                    "url": "https://www.theblock.co/post/262971/celsius-network-to-close-operations-by-end-of-february",
                    "content": "Celsius Network, the bankrupt crypto lender, said it will cease operations by the end of February as it wraps up its restructuring process.",
                    "published_at": datetime(2024, 2, 16, 14, 45, 0),
                    "journalist_id": michael.id if michael else None,
                    "outlet_id": the_block.id if the_block else None,
                    "topics": [crypto_topic, defi_topic],
                    "sentiment_score": -0.6,
                    "sentiment_label": "negative"
                },
                {
                    "title": "US Department of Justice files motion to seize BitMEX co-founder's stake in the exchange",
                    "url": "https://www.theblock.co/post/276201/doj-files-motion-to-seize-bitmex-cofounders-stake-in-the-exchange",
                    "content": "The U.S. Department of Justice has filed a motion to seize BitMEX co-founder Arthur Hayes' stake in the crypto derivatives exchange as part of ongoing legal proceedings.",
                    "published_at": datetime(2024, 3, 19, 10, 10, 0),
                    "journalist_id": michael.id if michael else None,
                    "outlet_id": the_block.id if the_block else None,
                    "topics": [exchange_topic, reg_topic],
                    "sentiment_score": -0.4,
                    "sentiment_label": "negative"
                }
            ]
            
            # Add articles to database
            articles_added = 0
            
            for article_data in block_articles:
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
            print(f"Successfully added {articles_added} recent articles from The Block (Jan-Mar 2024)")
            
            return True
        except Exception as e:
            print(f"Error adding Block articles: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    add_block_articles()