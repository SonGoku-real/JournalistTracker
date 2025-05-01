import spacy
import logging
import nltk
from app import db
from models import Article

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download necessary NLTK data (small resources)
try:
    nltk.download('punkt', quiet=True)
    logger.info("Successfully downloaded NLTK punkt tokenizer")
except Exception as e:
    logger.warning(f"Error downloading NLTK data: {e}")

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("Successfully loaded spaCy model")
except Exception as e:
    logger.warning(f"Error loading spaCy model: {e}")
    # Fallback to a basic model that should work
    nlp = spacy.blank("en")
    logger.info("Loaded fallback spaCy model")

def analyze_sentiment(text):
    """
    Analyze the sentiment of a text using spaCy.
    Returns a dictionary with sentiment score and label.
    """
    if not text:
        return {
            'score': 0.0,
            'label': 'neutral',
            'tone': 'unknown'
        }
    
    # Process the text with spaCy
    doc = nlp(text)
    
    # Basic sentiment analysis
    # This is a simplified approach - in a production system, you would use
    # a more sophisticated sentiment analysis model
    
    positive_words = set(['good', 'great', 'excellent', 'positive', 'amazing', 'wonderful', 
                        'fantastic', 'terrific', 'outstanding', 'superb', 'brilliant',
                        'happy', 'pleased', 'delighted', 'satisfied', 'impressed'])
    
    negative_words = set(['bad', 'terrible', 'awful', 'poor', 'negative', 'horrible', 
                        'dreadful', 'disappointing', 'inadequate', 'inferior', 'mediocre',
                        'annoyed', 'angry', 'upset', 'dissatisfied', 'troubled'])
    
    # Count positive and negative words
    positive_count = 0
    negative_count = 0
    
    for token in doc:
        if token.text.lower() in positive_words:
            positive_count += 1
        elif token.text.lower() in negative_words:
            negative_count += 1
    
    # Calculate a simple sentiment score
    total_words = len(doc)
    if total_words > 0:
        positive_score = positive_count / total_words
        negative_score = negative_count / total_words
        sentiment_score = positive_score - negative_score
    else:
        sentiment_score = 0.0
    
    # Determine sentiment label
    if sentiment_score > 0.05:
        sentiment_label = 'positive'
    elif sentiment_score < -0.05:
        sentiment_label = 'negative'
    else:
        sentiment_label = 'neutral'
    
    # Detect tone (simplified)
    # In a production system, you would use a more sophisticated tone detection model
    tone_words = {
        'analytical': set(['analyze', 'analysis', 'research', 'study', 'data', 'evidence', 'investigate']),
        'confident': set(['confident', 'certain', 'sure', 'definitely', 'absolutely', 'undoubtedly']),
        'tentative': set(['maybe', 'perhaps', 'possibly', 'might', 'could', 'uncertain', 'unclear']),
        'informative': set(['inform', 'information', 'explain', 'clarify', 'detail', 'elaborate']),
        'critical': set(['criticize', 'problem', 'issue', 'concern', 'flaw', 'defect', 'negative'])
    }
    
    tone_counts = {}
    for tone, words in tone_words.items():
        count = sum(1 for token in doc if token.text.lower() in words)
        tone_counts[tone] = count
    
    tone = max(tone_counts.items(), key=lambda x: x[1])[0] if any(tone_counts.values()) else 'neutral'
    
    return {
        'score': sentiment_score,
        'label': sentiment_label,
        'tone': tone
    }

def extract_topics(text):
    """
    Extract topics from text using spaCy.
    Returns a list of topic names.
    """
    if not text:
        return []
    
    # Process the text with spaCy
    doc = nlp(text)
    
    # Extract entities that could be topics
    topics = []
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'GPE', 'PERSON', 'EVENT', 'LAW', 'WORK_OF_ART']:
            topics.append(ent.text)
    
    # Also add noun chunks as potential topics
    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) <= 3:  # Limit to short phrases
            topics.append(chunk.text)
    
    # Return unique topics
    return list(set(topics))

def analyze_article(article):
    """
    Analyze an article and update its sentiment and topics.
    """
    if not article.content:
        logger.warning(f"Article {article.id} has no content to analyze")
        return
    
    try:
        # Analyze sentiment
        sentiment_result = analyze_sentiment(article.content)
        article.sentiment_score = sentiment_result['score']
        article.sentiment_label = sentiment_result['label']
        article.tone = sentiment_result['tone']
        
        # Extract topics
        topic_names = extract_topics(article.content)
        
        # Create or get Topic objects and associate with article
        from models import Topic
        
        for topic_name in topic_names:
            topic = Topic.query.filter_by(name=topic_name).first()
            if not topic:
                topic = Topic(name=topic_name)
                db.session.add(topic)
            
            if topic not in article.topics:
                article.topics.append(topic)
        
        # Update article in database
        db.session.commit()
        logger.info(f"Successfully analyzed article {article.id}")
        
    except Exception as e:
        logger.error(f"Error analyzing article {article.id}: {e}")
        db.session.rollback()

def analyze_all_articles():
    """
    Analyze all articles in the database that haven't been analyzed yet.
    """
    articles = Article.query.filter(
        (Article.sentiment_score.is_(None)) | 
        (Article.sentiment_label.is_(None))
    ).all()
    
    logger.info(f"Found {len(articles)} articles to analyze")
    
    for article in articles:
        analyze_article(article)
    
    logger.info("Finished analyzing articles")
