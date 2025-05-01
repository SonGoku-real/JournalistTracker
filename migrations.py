from app import app, db
from models import Journalist, Outlet, Article, Topic

def add_journalist_fields():
    """
    Add new fields to the journalist table
    """
    with app.app_context():
        conn = db.engine.connect()
        
        # Check if columns exist before adding them
        try:
            # Add region field
            conn.execute(db.text("ALTER TABLE journalist ADD COLUMN IF NOT EXISTS region VARCHAR(50)"))
            # Add verified field
            conn.execute(db.text("ALTER TABLE journalist ADD COLUMN IF NOT EXISTS verified BOOLEAN DEFAULT FALSE"))
            # Add last_contacted field
            conn.execute(db.text("ALTER TABLE journalist ADD COLUMN IF NOT EXISTS last_contacted TIMESTAMP"))
            # Add beat field
            conn.execute(db.text("ALTER TABLE journalist ADD COLUMN IF NOT EXISTS beat VARCHAR(100)"))
            
            conn.commit()
            print("Successfully added new fields to journalist table")
        except Exception as e:
            conn.rollback()
            print(f"Error adding new fields: {e}")
        finally:
            conn.close()

def populate_sample_regions():
    """
    Populate regions for existing journalists to provide initial data
    """
    regions = [
        "North America", 
        "Europe", 
        "Asia", 
        "Middle East",
        "Africa", 
        "Latin America", 
        "Oceania"
    ]
    
    with app.app_context():
        journalists = Journalist.query.all()
        count = 0
        
        try:
            for i, journalist in enumerate(journalists):
                if not journalist.region:
                    # Assign a region based on the journalist's location or in round-robin fashion
                    region = regions[i % len(regions)]
                    journalist.region = region
                    count += 1
            
            if count > 0:
                db.session.commit()
                print(f"Added region data to {count} journalists")
            else:
                print("No journalists needed region data")
        except Exception as e:
            db.session.rollback()
            print(f"Error populating regions: {e}")

def populate_journalist_details():
    """
    Update journalist records with more accurate information
    """
    with app.app_context():
        try:
            # For demo purposes, mark some journalists as verified
            verified_count = 0
            for i, journalist in enumerate(Journalist.query.all()):
                # Verify every other journalist
                if i % 2 == 0:
                    journalist.verified = True
                    verified_count += 1
                
                # Set beat field based on topics
                if journalist.topics:
                    # Use the first topic as the primary beat
                    journalist.beat = journalist.topics[0].name if journalist.topics else None
            
            db.session.commit()
            print(f"Verified {verified_count} journalists and updated beats")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating journalist details: {e}")

if __name__ == "__main__":
    # Run migrations
    add_journalist_fields()
    populate_sample_regions()
    populate_journalist_details()