from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models import Journalist, Article
from app import db

journalist_bp = Blueprint('journalists', __name__, url_prefix='/journalists')

@journalist_bp.route('/')
def list_journalists():
    # Get query parameters for filtering
    location = request.args.get('location', '')
    outlet = request.args.get('outlet', '')
    topic = request.args.get('topic', '')
    sentiment = request.args.get('sentiment', '')
    
    # Base query
    query = Journalist.query
    
    # Apply filters if provided
    if location:
        query = query.filter(Journalist.location.ilike(f'%{location}%'))
    
    if outlet:
        query = query.join(Journalist.outlet).filter(Outlet.name.ilike(f'%{outlet}%'))
    
    if topic:
        query = query.join(Journalist.topics).filter(Topic.name.ilike(f'%{topic}%'))
    
    # Get all journalists after filtering
    journalists = query.all()
    
    # Filter by sentiment (client-side filtering would be more efficient,
    # but this demonstrates the capability)
    if sentiment and sentiment in ['positive', 'negative', 'neutral']:
        # Filter journalists who predominantly write articles with the given sentiment
        filtered_journalists = []
        for journalist in journalists:
            sentiment_articles = [article for article in journalist.articles 
                                if article.sentiment_label == sentiment]
            if sentiment_articles and len(sentiment_articles) > len(journalist.articles) / 3:
                filtered_journalists.append(journalist)
        journalists = filtered_journalists
    
    return render_template('journalists/list.html', journalists=journalists)

@journalist_bp.route('/<int:journalist_id>')
def journalist_detail(journalist_id):
    journalist = Journalist.query.get_or_404(journalist_id)
    
    # Get articles by this journalist
    articles = Article.query.filter_by(journalist_id=journalist_id).order_by(Article.published_at.desc()).all()
    
    # Calculate sentiment distribution
    positive_count = sum(1 for article in articles if article.sentiment_label == 'positive')
    negative_count = sum(1 for article in articles if article.sentiment_label == 'negative')
    neutral_count = sum(1 for article in articles if article.sentiment_label == 'neutral')
    total_count = len(articles)
    
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
    for article in articles:
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
    
    return render_template('journalists/detail.html', 
                          journalist=journalist, 
                          articles=articles,
                          sentiment_data=sentiment_data,
                          topic_data=topic_data)

@journalist_bp.route('/export')
def export_journalists():
    journalists = Journalist.query.all()
    journalists_data = [journalist.to_dict() for journalist in journalists]
    return jsonify(journalists_data)
