from flask import Blueprint, render_template, redirect, url_for
from models import Journalist, Outlet, Article, Topic
from app import db
from utils.data_collection import populate_sample_data

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Check if we need to populate sample data (if the database is empty)
    journalist_count = Journalist.query.count()
    article_count = Article.query.count()
    
    if journalist_count == 0 or article_count == 0:
        populate_sample_data()
        return redirect(url_for('main.index'))
    
    # Get counts for dashboard
    outlet_count = Outlet.query.count()
    topic_count = Topic.query.count()
    
    # Get latest journalists
    latest_journalists = Journalist.query.order_by(Journalist.created_at.desc()).limit(5).all()
    
    # Get latest articles
    latest_articles = Article.query.order_by(Article.published_at.desc()).limit(5).all()
    
    # Get top topics by article count
    topics = Topic.query.all()
    topics_sorted = sorted(topics, key=lambda x: len(x.articles), reverse=True) if topics else []
    top_topics = topics_sorted[:10]
    
    # Get sentiment distribution
    positive_count = Article.query.filter(Article.sentiment_label == 'positive').count()
    negative_count = Article.query.filter(Article.sentiment_label == 'negative').count()
    neutral_count = Article.query.filter(Article.sentiment_label == 'neutral').count()
    
    return render_template('index.html', 
                          journalist_count=journalist_count,
                          outlet_count=outlet_count,
                          article_count=article_count,
                          topic_count=topic_count,
                          latest_journalists=latest_journalists,
                          latest_articles=latest_articles,
                          top_topics=top_topics,
                          sentiment_data={
                              'positive': positive_count,
                              'negative': negative_count,
                              'neutral': neutral_count
                          })
