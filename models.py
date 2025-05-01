from datetime import datetime
from app import db

# Define association tables for many-to-many relationships
journalist_topics = db.Table('journalist_topics',
    db.Column('journalist_id', db.Integer, db.ForeignKey('journalist.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True)
)

article_topics = db.Table('article_topics',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True)
)

class Journalist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    twitter_handle = db.Column(db.String(50), nullable=True)
    profile_image_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    outlet_id = db.Column(db.Integer, db.ForeignKey('outlet.id'), nullable=True)
    outlet = db.relationship('Outlet', back_populates='journalists')
    articles = db.relationship('Article', back_populates='journalist')
    topics = db.relationship('Topic', secondary=journalist_topics, back_populates='journalists')
    
    def __repr__(self):
        return f'<Journalist {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'twitter_handle': self.twitter_handle,
            'profile_image_url': self.profile_image_url,
            'bio': self.bio,
            'location': self.location,
            'outlet': self.outlet.name if self.outlet else None,
            'topics': [topic.name for topic in self.topics]
        }

class Outlet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    journalists = db.relationship('Journalist', back_populates='outlet')
    articles = db.relationship('Article', back_populates='outlet')
    
    def __repr__(self):
        return f'<Outlet {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website,
            'country': self.country,
            'description': self.description,
            'image_url': self.image_url,
            'journalist_count': len(self.journalists)
        }

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    published_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Sentiment analysis data
    sentiment_score = db.Column(db.Float, nullable=True)  # -1 to 1 (negative to positive)
    sentiment_label = db.Column(db.String(20), nullable=True)  # positive, negative, neutral
    tone = db.Column(db.String(50), nullable=True)  # analytical, confident, tentative, etc.
    
    # Relationships
    journalist_id = db.Column(db.Integer, db.ForeignKey('journalist.id'), nullable=True)
    journalist = db.relationship('Journalist', back_populates='articles')
    outlet_id = db.Column(db.Integer, db.ForeignKey('outlet.id'), nullable=True)
    outlet = db.relationship('Outlet', back_populates='articles')
    topics = db.relationship('Topic', secondary=article_topics, back_populates='articles')
    
    def __repr__(self):
        return f'<Article {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'published_at': self.published_at,
            'sentiment_score': self.sentiment_score,
            'sentiment_label': self.sentiment_label,
            'tone': self.tone,
            'journalist': self.journalist.name if self.journalist else None,
            'outlet': self.outlet.name if self.outlet else None,
            'topics': [topic.name for topic in self.topics]
        }

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    journalists = db.relationship('Journalist', secondary=journalist_topics, back_populates='topics')
    articles = db.relationship('Article', secondary=article_topics, back_populates='topics')
    
    def __repr__(self):
        return f'<Topic {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'journalist_count': len(self.journalists),
            'article_count': len(self.articles)
        }
