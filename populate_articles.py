from app import app
from utils.web_scraper import scrape_recent_crypto_articles

# Run within Flask app context
with app.app_context():
    print("\nPopulating database with real crypto articles...")
    result = scrape_recent_crypto_articles()
    print(result)
    
    print("\nArticle population complete!")