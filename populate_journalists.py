from app import app
from utils.web_scraper import scrape_coindesk_journalists

# Run within Flask app context
with app.app_context():
    print("Populating database with real crypto journalists...")
    result = scrape_coindesk_journalists()
    print(result)
    
    print("\nJournalist population complete!")