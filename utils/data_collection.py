import os
import json
import random
import datetime
import logging
from urllib.parse import urlparse
import requests
from app import db
from models import Journalist, Outlet, Article, Topic

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample profile images
JOURNALIST_IMAGES = [
    "/static/img/default-profile.svg",
    "/static/img/default-profile.svg",
    "/static/img/default-profile.svg",
    "/static/img/default-profile.svg",
    "/static/img/default-profile.svg",
    "/static/img/default-profile.svg"
]

# Sample outlet images
OUTLET_IMAGES = [
    "/static/img/default-outlet.svg",
    "/static/img/default-outlet.svg",
    "/static/img/default-outlet.svg",
    "/static/img/default-outlet.svg"
]

def get_news_articles(api_key=None, number=10):
    """
    Fetch news articles from NewsAPI.
    If no API key is provided, returns sample data.
    """
    if not api_key:
        logger.info("No NewsAPI key provided, using sample data")
        return generate_sample_articles(number)
    
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": api_key,
            "language": "en",
            "pageSize": number
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code != 200:
            logger.error(f"Error fetching news: {data.get('message', 'Unknown error')}")
            return generate_sample_articles(number)
        
        articles = data.get("articles", [])
        return articles
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return generate_sample_articles(number)

def generate_sample_articles(number=10):
    """
    Generate sample articles for demonstration.
    """
    sample_titles = [
        "New Climate Policy Announced by Government",
        "Tech Company Launches Revolutionary AI Product",
        "Sports Team Wins Championship After Decades",
        "Economic Growth Exceeds Expectations in Q3",
        "Health Researchers Discover Breakthrough Treatment",
        "Entertainment Industry Awards Ceremony Results",
        "Political Leaders Meet for International Summit",
        "Education Reform Bill Passes in Senate",
        "Scientific Study Reveals Surprising Findings",
        "Cultural Festival Celebrates Diversity and Inclusion",
        "Transportation Infrastructure Project Completed",
        "Environmental Protection Measures Implemented",
        "Financial Markets React to Policy Changes",
        "Social Media Platform Updates Privacy Settings",
        "Global Food Security Initiative Launched"
    ]
    
    sample_outlets = [
        "The Daily Chronicle",
        "Global News Network",
        "Tech Insider",
        "Business Daily",
        "Science Today",
        "World Politics Review",
        "The Health Report",
        "Environmental Observer",
        "Sports Coverage",
        "Arts & Culture Magazine"
    ]
    
    sample_content_templates = [
        "In a significant development, {subject} has announced {action}. This move is expected to {consequence}. Experts from {organization} believe this could lead to important changes. {quote}",
        "According to recent reports, {subject} is planning to {action}. This decision comes after careful consideration. Industry analysts at {organization} suggest this might {consequence}. {quote}",
        "Breaking news: {subject} has just {action}. This unexpected turn of events has caused {consequence}. Representatives from {organization} have stated that {quote}",
        "A new study by {organization} reveals that {subject} {action}. The findings indicate {consequence}. Researchers highlight that {quote}",
        "In an interview today, {subject} confirmed plans to {action}. This statement follows recent developments. Officials from {organization} responded saying {quote}"
    ]
    
    sample_subjects = [
        "the government", "leading researchers", "the company", "industry experts", 
        "international organizations", "local authorities", "the committee", 
        "policy makers", "community leaders", "scientific teams"
    ]
    
    sample_actions = [
        "implemented new policies", "discovered groundbreaking results", 
        "announced a major initiative", "released new findings", 
        "proposed significant changes", "launched an innovative project",
        "reached a consensus on important issues", "addressed ongoing concerns",
        "revealed unexpected data", "established new guidelines"
    ]
    
    sample_consequences = [
        "reshape the industry landscape", "have far-reaching implications",
        "affect numerous stakeholders", "change previous assumptions",
        "prompt further investigation", "require additional resources",
        "create new opportunities", "resolve longstanding problems",
        "establish new standards", "raise important questions"
    ]
    
    sample_organizations = [
        "the National Research Council", "leading universities", 
        "global think tanks", "industry associations", 
        "government agencies", "international committees",
        "independent research groups", "regulatory bodies",
        "specialized task forces", "professional organizations"
    ]
    
    sample_quotes = [
        "\"This represents a significant step forward in our understanding,\" said the lead researcher.",
        "\"We're excited about the possibilities this opens up for future development,\" according to the spokesperson.",
        "\"The implications of this cannot be overstated,\" commented one expert.",
        "\"We anticipate both challenges and opportunities as we move forward,\" noted the director.",
        "\"This aligns with our long-term goals for sustainable growth,\" explained the CEO.",
        "\"The data clearly supports our initial hypothesis,\" the team confirmed.",
        "\"We must proceed with caution while recognizing the potential benefits,\" advised the analyst.",
        "\"This breakthrough could transform how we approach these issues,\" suggested the consultant."
    ]
    
    articles = []
    
    for i in range(min(number, len(sample_titles))):
        content_template = random.choice(sample_content_templates)
        content = content_template.format(
            subject=random.choice(sample_subjects),
            action=random.choice(sample_actions),
            consequence=random.choice(sample_consequences),
            organization=random.choice(sample_organizations),
            quote=random.choice(sample_quotes)
        )
        
        # Create random date within the last 30 days
        days_ago = random.randint(0, 30)
        published_date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).isoformat()
        
        article = {
            "title": sample_titles[i],
            "source": {"name": random.choice(sample_outlets)},
            "author": None,  # Will be populated from our journalist database
            "publishedAt": published_date,
            "url": f"https://example.com/article/{i+1}",
            "content": content
        }
        
        articles.append(article)
    
    return articles

def create_sample_outlets():
    """
    Create sample media outlets for demonstration.
    """
    sample_outlets = [
        {
            "name": "The Daily Chronicle",
            "website": "https://dailychronicle.example.com",
            "country": "United States",
            "description": "A leading daily newspaper covering national and international news, politics, business, and culture.",
            "image_url": OUTLET_IMAGES[0]
        },
        {
            "name": "Global News Network",
            "website": "https://gnn.example.com",
            "country": "United Kingdom",
            "description": "An international news organization providing 24/7 coverage of global events and breaking news.",
            "image_url": OUTLET_IMAGES[1]
        },
        {
            "name": "Tech Insider",
            "website": "https://techinsider.example.com",
            "country": "United States",
            "description": "The premier source for technology news, reviews, and analysis of industry trends.",
            "image_url": OUTLET_IMAGES[2]
        },
        {
            "name": "Business Daily",
            "website": "https://businessdaily.example.com",
            "country": "Canada",
            "description": "Comprehensive coverage of financial markets, corporate news, and economic developments.",
            "image_url": OUTLET_IMAGES[3]
        },
        {
            "name": "Science Today",
            "website": "https://sciencetoday.example.com",
            "country": "Germany",
            "description": "Reporting on the latest scientific research, discoveries, and technological innovations.",
            "image_url": OUTLET_IMAGES[0]
        },
        {
            "name": "World Politics Review",
            "website": "https://worldpolitics.example.com",
            "country": "France",
            "description": "In-depth analysis of international relations, geopolitical developments, and diplomatic affairs.",
            "image_url": OUTLET_IMAGES[1]
        },
        {
            "name": "The Health Report",
            "website": "https://healthreport.example.com",
            "country": "Australia",
            "description": "Covering medical research, public health issues, and healthcare policy developments.",
            "image_url": OUTLET_IMAGES[2]
        },
        {
            "name": "Environmental Observer",
            "website": "https://envobserver.example.com",
            "country": "Sweden",
            "description": "Focused on environmental news, climate change, conservation efforts, and sustainability.",
            "image_url": OUTLET_IMAGES[3]
        }
    ]
    
    outlets = []
    
    for outlet_data in sample_outlets:
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
            image_url=outlet_data["image_url"]
        )
        
        db.session.add(outlet)
        outlets.append(outlet)
    
    db.session.commit()
    return outlets

def create_sample_journalists(outlets):
    """
    Create sample journalists for demonstration.
    """
    sample_journalists = [
        {
            "name": "Alex Johnson",
            "email": "alex.johnson@example.com",
            "twitter_handle": "@alexjreports",
            "bio": "Senior political correspondent with over 15 years of experience covering national politics and policy issues.",
            "location": "Washington, D.C."
        },
        {
            "name": "Maya Rodriguez",
            "email": "maya.rodriguez@example.com",
            "twitter_handle": "@mayar_tech",
            "bio": "Technology reporter specializing in AI, cybersecurity, and emerging tech trends. Previously at Tech Monthly.",
            "location": "San Francisco, CA"
        },
        {
            "name": "James Chen",
            "email": "james.chen@example.com",
            "twitter_handle": "@jchen_business",
            "bio": "Finance and economics journalist with expertise in market analysis and corporate reporting.",
            "location": "New York, NY"
        },
        {
            "name": "Sophia Williams",
            "email": "sophia.williams@example.com",
            "twitter_handle": "@sophiascience",
            "bio": "Science correspondent covering breakthrough research in medicine, physics, and environmental science.",
            "location": "Boston, MA"
        },
        {
            "name": "Omar Hassan",
            "email": "omar.hassan@example.com",
            "twitter_handle": "@ohassan_global",
            "bio": "International affairs reporter with experience in conflict zones across the Middle East and Africa.",
            "location": "London, UK"
        },
        {
            "name": "Priya Sharma",
            "email": "priya.sharma@example.com",
            "twitter_handle": "@priyasharma_env",
            "bio": "Environmental journalist focused on climate change policy, conservation efforts, and sustainable development.",
            "location": "Stockholm, Sweden"
        }
    ]
    
    journalists = []
    
    for i, journalist_data in enumerate(sample_journalists):
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
            outlet_id=outlets[i % len(outlets)].id,  # Assign to an outlet
            profile_image_url=JOURNALIST_IMAGES[i % len(JOURNALIST_IMAGES)]
        )
        
        db.session.add(journalist)
        journalists.append(journalist)
    
    db.session.commit()
    return journalists

def create_sample_topics():
    """
    Create sample topics for demonstration.
    """
    sample_topics = [
        {"name": "Politics", "description": "Political news, policy discussions, and government affairs"},
        {"name": "Technology", "description": "News about tech companies, products, and innovations"},
        {"name": "Business", "description": "Corporate news, financial markets, and economic trends"},
        {"name": "Science", "description": "Scientific research, discoveries, and innovations"},
        {"name": "Health", "description": "Medical research, public health, and healthcare"},
        {"name": "Environment", "description": "Climate change, conservation, and sustainability"},
        {"name": "Sports", "description": "Athletic competitions, teams, and sports business"},
        {"name": "Entertainment", "description": "Movies, music, celebrities, and media industry"},
        {"name": "Education", "description": "Schools, universities, teaching, and learning"},
        {"name": "International", "description": "Global affairs, diplomacy, and world events"}
    ]
    
    topics = []
    
    for topic_data in sample_topics:
        # Check if topic already exists
        existing_topic = Topic.query.filter_by(name=topic_data["name"]).first()
        if existing_topic:
            topics.append(existing_topic)
            continue
        
        # Create new topic
        topic = Topic(
            name=topic_data["name"],
            description=topic_data["description"]
        )
        
        db.session.add(topic)
        topics.append(topic)
    
    db.session.commit()
    return topics

def process_article(article_data, journalists, topics):
    """
    Process an article from the API or sample data and save to database.
    """
    # Extract fields from the article data
    title = article_data.get("title", "Untitled")
    url = article_data.get("url", "")
    content = article_data.get("content", "")
    source_name = article_data.get("source", {}).get("name", "")
    
    # Parse published date
    published_at_str = article_data.get("publishedAt", "")
    try:
        published_at = datetime.datetime.fromisoformat(published_at_str.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        published_at = datetime.datetime.utcnow()
    
    # Check if article already exists
    existing_article = Article.query.filter_by(url=url).first()
    if existing_article:
        return existing_article
    
    # Find the outlet
    outlet = Outlet.query.filter_by(name=source_name).first()
    
    # If outlet doesn't exist, create it
    if not outlet:
        outlet = Outlet(
            name=source_name,
            website=f"https://{urlparse(url).netloc}" if url else "",
            image_url=random.choice(OUTLET_IMAGES)
        )
        db.session.add(outlet)
        db.session.commit()
    
    # Randomly assign a journalist if author is not specified
    journalist = None
    author_name = article_data.get("author")
    
    if author_name:
        # Look for journalist by name
        journalist = Journalist.query.filter_by(name=author_name).first()
    
    if not journalist:
        # Assign random journalist from the same outlet if possible
        outlet_journalists = Journalist.query.filter_by(outlet_id=outlet.id).all()
        if outlet_journalists:
            journalist = random.choice(outlet_journalists)
        elif journalists:  # Fallback to any journalist
            journalist = random.choice(journalists)
    
    # Create the article
    article = Article(
        title=title,
        url=url,
        content=content,
        published_at=published_at,
        journalist_id=journalist.id if journalist else None,
        outlet_id=outlet.id
    )
    
    # Randomly assign some topics
    num_topics = random.randint(1, 3)
    random_topics = random.sample(topics, min(num_topics, len(topics)))
    article.topics = random_topics
    
    db.session.add(article)
    db.session.commit()
    
    # Analyze article sentiment and update
    from utils.nlp_utils import analyze_article
    analyze_article(article)
    
    return article

def fetch_and_process_articles(api_key=None, number=10):
    """
    Fetch articles from the API and process them.
    """
    # Get journalists and topics for association
    journalists = Journalist.query.all()
    topics = Topic.query.all()
    
    # Fetch articles from the API (or get sample data)
    articles_data = get_news_articles(api_key, number)
    
    processed_articles = []
    for article_data in articles_data:
        article = process_article(article_data, journalists, topics)
        processed_articles.append(article)
    
    return processed_articles

def populate_sample_data():
    """
    Populate the database with sample data for demonstration.
    """
    logger.info("Populating database with sample data")
    
    # Create sample outlets
    outlets = create_sample_outlets()
    logger.info(f"Created {len(outlets)} sample outlets")
    
    # Create sample journalists
    journalists = create_sample_journalists(outlets)
    logger.info(f"Created {len(journalists)} sample journalists")
    
    # Create sample topics
    topics = create_sample_topics()
    logger.info(f"Created {len(topics)} sample topics")
    
    # Fetch and process articles
    api_key = os.environ.get("NEWS_API_KEY")
    articles = fetch_and_process_articles(api_key, 20)
    logger.info(f"Processed {len(articles)} articles")
    
    return True
