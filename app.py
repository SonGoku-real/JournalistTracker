import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the Base class
db = SQLAlchemy(model_class=Base)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///journalist_tracker.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database with the app
db.init_app(app)

# Register routes
with app.app_context():
    # Import models
    import models  # noqa: F401
    
    # Import routes
    from routes.main_routes import main_bp
    from routes.journalist_routes import journalist_bp
    from routes.outlet_routes import outlet_bp
    from routes.analytics_routes import analytics_bp
    from routes.search_routes import search_bp
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(journalist_bp)
    app.register_blueprint(outlet_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(search_bp)
    
    # Create database tables
    db.create_all()
    logger.info("Database tables created")
