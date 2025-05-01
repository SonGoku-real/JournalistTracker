from app import app
from utils.crypto_data import populate_all_crypto_data

# Run within Flask app context
with app.app_context():
    print("Populating database with real crypto journalists, outlets, topics, and articles...")
    result = populate_all_crypto_data()
    if result:
        print("Successfully populated all crypto data!")
    else:
        print("Failed to populate crypto data. Check the logs for details.")
    