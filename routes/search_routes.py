from flask import Blueprint, render_template, request, jsonify
from models import Journalist, Outlet, Article, Topic
from app import db
from sqlalchemy import or_

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/')
def search_page():
    # Get all topics for filtering
    topics = Topic.query.order_by(Topic.name).all()
    
    # Get all countries for filtering
    countries = db.session.query(Outlet.country).distinct().all()
    countries = [country[0] for country in countries if country[0]]
    
    # Get all regions for filtering
    regions = db.session.query(Journalist.region).distinct().all()
    regions = [region[0] for region in regions if region[0]]
    
    return render_template('search/search.html', topics=topics, countries=countries, regions=regions)

@search_bp.route('/results')
def search_results():
    # Get search parameters
    query = request.args.get('q', '')
    entity_type = request.args.get('type', 'all')
    topic = request.args.get('topic', '')
    country = request.args.get('country', '')
    region = request.args.get('region', '')
    sentiment = request.args.get('sentiment', '')
    
    results = {
        'journalists': [],
        'outlets': [],
        'articles': []
    }
    
    # Search journalists
    if entity_type in ['all', 'journalists']:
        journalist_query = Journalist.query
        
        if query:
            journalist_query = journalist_query.filter(
                or_(
                    Journalist.name.ilike(f'%{query}%'),
                    Journalist.bio.ilike(f'%{query}%'),
                    Journalist.location.ilike(f'%{query}%'),
                    Journalist.email.ilike(f'%{query}%'),
                    Journalist.twitter_handle.ilike(f'%{query}%'),
                    Journalist.beat.ilike(f'%{query}%')
                )
            )
        
        if topic:
            journalist_query = journalist_query.join(Journalist.topics).filter(Topic.name == topic)
        
        if country:
            journalist_query = journalist_query.join(Journalist.outlet).filter(Outlet.country == country)
        
        if region:
            journalist_query = journalist_query.filter(Journalist.region == region)
            
        # Add verification filter if needed
        # if verified_only:
        #     journalist_query = journalist_query.filter(Journalist.verified == True)
        
        journalists = journalist_query.all()
        
        # Filter by sentiment (this is more complex and would need a more sophisticated query in production)
        if sentiment and sentiment in ['positive', 'negative', 'neutral']:
            filtered_journalists = []
            for journalist in journalists:
                sentiment_articles = [article for article in journalist.articles 
                                    if article.sentiment_label == sentiment]
                if sentiment_articles and len(sentiment_articles) > len(journalist.articles) / 3:
                    filtered_journalists.append(journalist)
            journalists = filtered_journalists
        
        results['journalists'] = [journalist.to_dict() for journalist in journalists]
    
    # Search outlets
    if entity_type in ['all', 'outlets']:
        outlet_query = Outlet.query
        
        if query:
            outlet_query = outlet_query.filter(
                or_(
                    Outlet.name.ilike(f'%{query}%'),
                    Outlet.description.ilike(f'%{query}%'),
                    Outlet.website.ilike(f'%{query}%')
                )
            )
        
        if country:
            outlet_query = outlet_query.filter(Outlet.country == country)
        
        if region and topic:
            # Outlets with journalists in the specified region and topic
            outlet_query = outlet_query.join(Outlet.journalists).filter(
                Journalist.region == region
            ).join(Journalist.topics).filter(Topic.name == topic)
        elif region:
            # Outlets with journalists in the specified region
            outlet_query = outlet_query.join(Outlet.journalists).filter(Journalist.region == region)
        elif topic:
            # This is a complex query - outlets that have journalists who write about this topic
            outlet_query = outlet_query.join(Outlet.journalists).join(Journalist.topics).filter(Topic.name == topic)
        
        outlets = outlet_query.all()
        results['outlets'] = [outlet.to_dict() for outlet in outlets]
    
    # Search articles
    if entity_type in ['all', 'articles']:
        article_query = Article.query
        
        if query:
            article_query = article_query.filter(
                or_(
                    Article.title.ilike(f'%{query}%'),
                    Article.content.ilike(f'%{query}%')
                )
            )
        
        if topic:
            article_query = article_query.join(Article.topics).filter(Topic.name == topic)
        
        if country:
            article_query = article_query.join(Article.outlet).filter(Outlet.country == country)
        
        if region:
            article_query = article_query.join(Article.journalist).filter(Journalist.region == region)
            
        if sentiment:
            article_query = article_query.filter(Article.sentiment_label == sentiment)
        
        articles = article_query.all()
        results['articles'] = [article.to_dict() for article in articles]
    
    # If this is an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(results)
    
    # Otherwise render the template with results
    return render_template('search/results.html', 
                          results=results, 
                          query=query, 
                          entity_type=entity_type,
                          topic=topic,
                          country=country,
                          region=region,
                          sentiment=sentiment)

@search_bp.route('/export')
def export_results():
    # Similar logic to search_results, but always returns JSON
    query = request.args.get('q', '')
    entity_type = request.args.get('type', 'all')
    topic = request.args.get('topic', '')
    country = request.args.get('country', '')
    region = request.args.get('region', '')
    sentiment = request.args.get('sentiment', '')
    
    results = {
        'journalists': [],
        'outlets': [],
        'articles': []
    }
    
    # Search journalists
    if entity_type in ['all', 'journalists']:
        journalist_query = Journalist.query
        
        if query:
            journalist_query = journalist_query.filter(
                or_(
                    Journalist.name.ilike(f'%{query}%'),
                    Journalist.bio.ilike(f'%{query}%'),
                    Journalist.location.ilike(f'%{query}%'),
                    Journalist.email.ilike(f'%{query}%'),
                    Journalist.twitter_handle.ilike(f'%{query}%'),
                    Journalist.beat.ilike(f'%{query}%')
                )
            )
        
        if topic:
            journalist_query = journalist_query.join(Journalist.topics).filter(Topic.name == topic)
        
        if country:
            journalist_query = journalist_query.join(Journalist.outlet).filter(Outlet.country == country)
        
        if region:
            journalist_query = journalist_query.filter(Journalist.region == region)
            
        journalists = journalist_query.all()
        results['journalists'] = [journalist.to_dict() for journalist in journalists]
    
    # Search outlets
    if entity_type in ['all', 'outlets']:
        outlet_query = Outlet.query
        
        if query:
            outlet_query = outlet_query.filter(
                or_(
                    Outlet.name.ilike(f'%{query}%'),
                    Outlet.description.ilike(f'%{query}%'),
                    Outlet.website.ilike(f'%{query}%')
                )
            )
        
        if country:
            outlet_query = outlet_query.filter(Outlet.country == country)
        
        if region and topic:
            # Outlets with journalists in the specified region and topic
            outlet_query = outlet_query.join(Outlet.journalists).filter(
                Journalist.region == region
            ).join(Journalist.topics).filter(Topic.name == topic)
        elif region:
            # Outlets with journalists in the specified region
            outlet_query = outlet_query.join(Outlet.journalists).filter(Journalist.region == region)
        elif topic:
            # This is a complex query - outlets that have journalists who write about this topic
            outlet_query = outlet_query.join(Outlet.journalists).join(Journalist.topics).filter(Topic.name == topic)
        
        outlets = outlet_query.all()
        results['outlets'] = [outlet.to_dict() for outlet in outlets]
    
    # Search articles
    if entity_type in ['all', 'articles']:
        article_query = Article.query
        
        if query:
            article_query = article_query.filter(
                or_(
                    Article.title.ilike(f'%{query}%'),
                    Article.content.ilike(f'%{query}%')
                )
            )
        
        if topic:
            article_query = article_query.join(Article.topics).filter(Topic.name == topic)
        
        if country:
            article_query = article_query.join(Article.outlet).filter(Outlet.country == country)
        
        if region:
            article_query = article_query.join(Article.journalist).filter(Journalist.region == region)
            
        if sentiment:
            article_query = article_query.filter(Article.sentiment_label == sentiment)
        
        articles = article_query.all()
        results['articles'] = [article.to_dict() for article in articles]
    
    return jsonify(results)