import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Stripe Configuration
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
    
    # Stripe Price IDs
    STRIPE_LIFETIME_PRICE_ID = os.getenv('STRIPE_LIFETIME_PRICE_ID', '')
    STRIPE_MONTHLY_PRICE_ID = os.getenv('STRIPE_MONTHLY_PRICE_ID', '')
    STRIPE_YEARLY_PRICE_ID = os.getenv('STRIPE_YEARLY_PRICE_ID', '')
    
    # Google AdSense
    ADSENSE_CLIENT_ID = os.getenv('ADSENSE_CLIENT_ID', 'ca-pub-XXXXXXXXXX')
    
    # Premium Token Settings
    PREMIUM_TOKEN_EXPIRY_DAYS = 36500  # ~100 years for "lifetime" access
    
    # Database - use /tmp on Vercel (read-only filesystem except /tmp)
    _is_vercel = os.getenv('VERCEL') or os.getenv('VERCEL_ENV')
    DATABASE_PATH = '/tmp/premium_users.db' if _is_vercel else os.path.join(os.path.dirname(__file__), 'premium_users.db')
    
    # App Settings
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

# Config dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(env='development'):
    """Get configuration based on environment"""
    return config.get(env, config['default'])
