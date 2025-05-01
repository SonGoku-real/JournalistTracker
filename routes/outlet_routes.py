from flask import Blueprint, render_template, request, jsonify
from models import Outlet, Journalist, Article, Topic
from app import db

outlet_bp = Blueprint('outlets', __name__, url_prefix='/outlets')

@outlet_bp.route('/')
def list_outlets():
    # Get query parameters for filtering
    country = request.args.get('country', '')
    topic = request.args.get('topic', '')
    
    # Base query
    query = Outlet.query
    
    # Apply filters if provided
    if country:
        query = query.filter(Outlet.country.ilike(f'%{country}%'))
    
    if topic:
        query = query.join(Outlet.journalists).join(Journalist.topics).filter(Topic.name.ilike(f'%{topic}%'))
    
    # Get all outlets after filtering
    outlets = query.all()
    
    # Get countries for filter dropdown
    countries = db.session.query(Outlet.country).distinct().all()
    countries = [country[0] for country in countries if country[0]]
    
    return render_template('outlets/list.html', outlets=outlets, countries=countries)

@outlet_bp.route('/<int:outlet_id>')
def outlet_detail(outlet_id):
    outlet = Outlet.query.get_or_404(outlet_id)
    
    # Get journalists for this outlet
    journalists = Journalist.query.filter_by(outlet_id=outlet_id).all()
    
    # Get articles for this outlet
    articles = Article.query.filter_by(outlet_id=outlet_id).order_by(Article.published_at.desc()).limit(10).all()
    
    # Calculate sentiment distribution for outlet articles
    outlet_articles = Article.query.filter_by(outlet_id=outlet_id).all()
    positive_count = sum(1 for article in outlet_articles if article.sentiment_label == 'positive')
    negative_count = sum(1 for article in outlet_articles if article.sentiment_label == 'negative')
    neutral_count = sum(1 for article in outlet_articles if article.sentiment_label == 'neutral')
    total_count = len(outlet_articles)
    
    # Prepare data for Charts.js
    sentiment_data = {
        'labels': ['Positive', 'Negative', 'Neutral'],
        'data': [
            round(positive_count / total_count * 100 if total_count > 0 else 0, 1),
            round(negative_count / total_count * 100 if total_count > 0 else 0, 1),
            round(neutral_count / total_count * 100 if total_count > 0 else 0, 1)
        ]
    }
    
    # Get topic distribution
    topic_counts = {}
    for article in outlet_articles:
        for topic in article.topics:
            if topic.name in topic_counts:
                topic_counts[topic.name] += 1
            else:
                topic_counts[topic.name] = 1
    
    # Sort topics by count
    sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
    topic_data = {
        'labels': [item[0] for item in sorted_topics[:5]],
        'data': [item[1] for item in sorted_topics[:5]]
    }
    
    return render_template('outlets/detail.html', 
                          outlet=outlet, 
                          journalists=journalists,
                          articles=articles,
                          sentiment_data=sentiment_data,
                          topic_data=topic_data)

@outlet_bp.route('/export')
def export_outlets():
    outlets = Outlet.query.all()
    outlets_data = [outlet.to_dict() for outlet in outlets]
    return jsonify(outlets_data)
