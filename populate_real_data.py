from app import app
from utils.web_scraper import scrape_coindesk_journalists, scrape_recent_crypto_articles

# Run within Flask app context
with app.app_context():
    print("Populating database with real crypto journalists...")
    result1 = scrape_coindesk_journalists()
    print(result1)
    
    print("\nPopulating database with real crypto articles...")
    result2 = scrape_recent_crypto_articles()
    print(result2)
    
    print("\nDatabase population complete!")