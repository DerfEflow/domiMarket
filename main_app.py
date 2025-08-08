import os
import logging
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from dotenv import load_dotenv
from models import db, User
from auth import auth
from dashboard import dashboard
from services.trend_api_endpoints import trend_api

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # type: ignore
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(dashboard)
    app.register_blueprint(trend_api)
    
    # Register new Sell Profile API
    try:
        from services.sell_profile_api_endpoints import sell_profile_api
        app.register_blueprint(sell_profile_api)
    except ImportError as e:
        logging.warning(f"Could not import sell_profile_api: {e}")
    
    # Register Stripe Payment System
    try:
        from services.stripe_payment_system import payment_bp
        app.register_blueprint(payment_bp)
    except ImportError as e:
        logging.warning(f"Could not import payment system: {e}")
    
    # Trends API already registered above
    
    # Register licensing API
    try:
        from services.licensing_api import licensing_api
        app.register_blueprint(licensing_api)
    except ImportError:
        pass
    
    # Main routes
    @app.route('/')
    def index():
        """Landing page with marketing and signup"""
        return render_template('index.html')
    
    @app.route('/features')
    def features():
        """Features page"""
        return render_template('features.html')
    
    @app.route('/faq')
    def faq_main():
        """FAQ page"""
        return render_template('faq.html')
    
    @app.route('/terms')
    def terms():
        """Terms of service page"""
        return render_template('terms.html')
    
    @app.route('/privacy')
    def privacy():
        """Privacy policy page"""
        return render_template('privacy.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)