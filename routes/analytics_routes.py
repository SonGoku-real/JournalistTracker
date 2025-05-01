from flask import Blueprint, render_template, jsonify
from models import Journalist, Outlet, Article, Topic
from app import db
from sqlalchemy import func
import json

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/')
def dashboard():
    # Get counts for dashboard
    journalist_count = Journalist.query.count()
    outlet_count = Outlet.query.count()
    article_count = Article.query.count()
    topic_count = Topic.query.count()
    
    # Get sentiment distribution
    positive_count = Article.query.filter(Article.sentiment_label == 'positive').count()
    negative_count = Article.query.filter(Article.sentiment_label == 'negative').count()
    neutral_count = Article.query.filter(Article.sentiment_label == 'neutral').count()
    total_count = positive_count + negative_count + neutral_count
    
    sentiment_data = {
        'labels': ['Positive', 'Negative', 'Neutral'],
        'data': [
            round(positive_count / total_count * 100 if total_count > 0 else 0, 1),
            round(negative_count / total_count * 100 if total_count > 0 else 0, 1),
            round(neutral_count / total_count * 100 if total_count > 0 else 0, 1)
        ]
    }
    
    # Get topic distribution
    topics = Topic.query.all()
    topic_data = {
        'labels': [topic.name for topic in topics[:10]],
        'data': [len(topic.articles) for topic in topics[:10]]
    }
    
    # Get outlet distribution
    outlets = Outlet.query.all()
    outlet_data = {
        'labels': [outlet.name for outlet in outlets[:10]],
        'data': [len(outlet.journalists) for outlet in outlets[:10]]
    }
    
    # Get tone distribution
    tones = db.session.query(Article.tone, func.count(Article.id)).\
        filter(Article.tone.isnot(None)).\
        group_by(Article.tone).\
        order_by(func.count(Article.id).desc()).\
        all()
    
    tone_data = {
        'labels': [tone[0] for tone in tones],
        'data': [tone[1] for tone in tones]
    }
    
    return render_template('analytics/dashboard.html',
                          journalist_count=journalist_count,
                          outlet_count=outlet_count,
                          article_count=article_count,
                          topic_count=topic_count,
                          sentiment_data=json.dumps(sentiment_data),
                          topic_data=json.dumps(topic_data),
                          outlet_data=json.dumps(outlet_data),
                          tone_data=json.dumps(tone_data))

@analytics_bp.route('/data/sentiment')
def sentiment_data():
    # Get sentiment data over time (last 30 days)
    sentiment_over_time = db.session.query(
        func.date(Article.published_at),
        func.count(Article.id).filter(Article.sentiment_label == 'positive'),
        func.count(Article.id).filter(Article.sentiment_label == 'negative'),
        func.count(Article.id).filter(Article.sentiment_label == 'neutral')
    ).group_by(func.date(Article.published_at)).order_by(func.date(Article.published_at)).all()
    
    data = {
        'dates': [row[0].strftime('%Y-%m-%d') if row[0] else 'Unknown' for row in sentiment_over_time],
        'positive': [row[1] for row in sentiment_over_time],
        'negative': [row[2] for row in sentiment_over_time],
        'neutral': [row[3] for row in sentiment_over_time]
    }
    
    return jsonify(data)

@analytics_bp.route('/data/topics')
def topic_data():
    # Get topic distribution
    topics = Topic.query.all()
    topics_sorted = sorted(topics, key=lambda x: len(x.articles), reverse=True)
    
    data = {
        'labels': [topic.name for topic in topics_sorted[:15]],
        'data': [len(topic.articles) for topic in topics_sorted[:15]]
    }
    
    return jsonify(data)

@analytics_bp.route('/data/outlets')
def outlet_data():
    # Get outlet distribution
    outlets = Outlet.query.all()
    outlets_sorted = sorted(outlets, key=lambda x: len(x.journalists), reverse=True)
    
    data = {
        'labels': [outlet.name for outlet in outlets_sorted[:15]],
        'data': [len(outlet.journalists) for outlet in outlets_sorted[:15]]
    }
    
    return jsonify(data)
