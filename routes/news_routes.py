from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from models import Article, Topic, db
from sqlalchemy import desc
import logging
import importlib

news_bp = Blueprint('news', __name__, url_prefix='/news')
logger = logging.getLogger(__name__)

@news_bp.route('/')
def latest_news():
    """
    Display the latest news articles with filter options.
    """
    # Get query parameters for filtering
    keyword = request.args.get('keyword', '')
    topic = request.args.get('topic', '')
    days = request.args.get('days', '7')  # Default to last 7 days
    
    try:
        days = int(days)
    except ValueError:
        days = 7
    
    # Get available topics for filter dropdown
    topics = Topic.query.all()
    
    # Base query
    query = Article.query
    
    # Apply filters
    if keyword:
        query = query.filter(
            (Article.title.ilike(f'%{keyword}%')) | 
            (Article.content.ilike(f'%{keyword}%'))
        )
    
    if topic:
        query = query.join(Article.topics).filter(Topic.name == topic)
    
    # Get the latest articles
    articles = query.order_by(desc(Article.published_at)).limit(50).all()
    
    return render_template('news/latest.html', 
                          articles=articles, 
                          topics=topics,
                          current_keyword=keyword,
                          current_topic=topic,
                          current_days=days)

@news_bp.route('/refresh')
def refresh_news():
    """
    Manually trigger a refresh of the news feed.
    """
    days = request.args.get('days', '1')
    try:
        days = int(days)
    except ValueError:
        days = 1
    
    try:
        # Dynamically import to avoid circular imports
        news_fetcher = importlib.import_module('utils.news_fetcher')
        count = news_fetcher.update_news_feed(days=days)
        return jsonify({
            'success': True,
            'message': f'Successfully added {count} new articles',
            'count': count
        })
    except Exception as e:
        logger.error(f"Error refreshing news: {e}")
        return jsonify({
            'success': False,
            'message': f'Error refreshing news: {str(e)}'
        }), 500

@news_bp.route('/keywords')
def manage_keywords():
    """
    View to manage tracked keywords.
    """
    # In a future implementation, this would allow managing custom keywords
    # For now, we show the predefined keywords from news_fetcher.py
    # Dynamically import to avoid circular imports
    news_fetcher = importlib.import_module('utils.news_fetcher')
    
    return render_template('news/keywords.html', keywords=news_fetcher.CRYPTO_KEYWORDS)