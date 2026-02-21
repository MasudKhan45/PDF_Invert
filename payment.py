import stripe
import secrets
import sqlite3
from datetime import datetime, timedelta
from flask import jsonify
from config import Config

# Initialize Stripe
stripe.api_key = Config.STRIPE_SECRET_KEY

def init_database():
    """Initialize SQLite database for premium tokens"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS premium_tokens (
            token TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            subscription_type TEXT,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    conn.commit()
    conn.close()

def generate_premium_token():
    """Generate a secure random token for premium access"""
    return secrets.token_urlsafe(32)

def create_checkout_session(price_id, subscription_type='lifetime'):
    """
    Create a Stripe Checkout session for premium purchase
    
    Args:
        price_id: Stripe Price ID for the product
        subscription_type: 'lifetime', 'monthly', or 'yearly'
    
    Returns:
        dict: Session data with checkout URL
    """
    try:
        # Determine mode based on subscription type
        mode = 'payment' if subscription_type == 'lifetime' else 'subscription'
        
        # Create checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode=mode,
            success_url='http://localhost:5000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:5000/?canceled=true',
            metadata={
                'subscription_type': subscription_type
            }
        )
        
        return {
            'session_id': session.id,
            'url': session.url
        }
    
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return None

def store_premium_token(token, subscription_type='lifetime'):
    """
    Store premium token in database
    
    Args:
        token: The premium access token
        subscription_type: Type of subscription
    """
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Calculate expiry date
    if subscription_type == 'lifetime':
        expires_at = datetime.now() + timedelta(days=Config.PREMIUM_TOKEN_EXPIRY_DAYS)
    elif subscription_type == 'monthly':
        expires_at = datetime.now() + timedelta(days=30)
    elif subscription_type == 'yearly':
        expires_at = datetime.now() + timedelta(days=365)
    else:
        expires_at = datetime.now() + timedelta(days=Config.PREMIUM_TOKEN_EXPIRY_DAYS)
    
    cursor.execute('''
        INSERT INTO premium_tokens (token, expires_at, subscription_type)
        VALUES (?, ?, ?)
    ''', (token, expires_at, subscription_type))
    
    conn.commit()
    conn.close()

def verify_premium_token(token):
    """
    Verify if a premium token is valid and active
    
    Args:
        token: The token to verify
    
    Returns:
        bool: True if valid and active, False otherwise
    """
    if not token:
        return False
    
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT expires_at, is_active 
        FROM premium_tokens 
        WHERE token = ?
    ''', (token,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return False
    
    expires_at, is_active = result
    
    # Check if token is active and not expired
    if is_active == 1 and datetime.now() < datetime.fromisoformat(expires_at):
        return True
    
    return False

def handle_stripe_webhook(payload, sig_header):
    """
    Handle Stripe webhook events
    
    Args:
        payload: Raw request body
        sig_header: Stripe signature header
    
    Returns:
        dict: Response data
    """
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, Config.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return {'error': 'Invalid payload'}, 400
    except stripe.error.SignatureVerificationError:
        return {'error': 'Invalid signature'}, 400
    
    # Handle checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Generate and store premium token
        token = generate_premium_token()
        subscription_type = session['metadata'].get('subscription_type', 'lifetime')
        store_premium_token(token, subscription_type)
        
        # In production, you would email this token to the customer
        # For now, we'll return it in the success page URL
        print(f"Premium token created: {token}")
        
        return {'status': 'success', 'token': token}, 200
    
    return {'status': 'ignored'}, 200

def get_pricing_info():
    """Get pricing information for all tiers"""
    return {
        'lifetime': {
            'price': '$4.99',
            'price_id': Config.STRIPE_LIFETIME_PRICE_ID,
            'name': 'Lifetime Ad-Free',
            'description': 'One-time payment',
            'features': [
                'No ads ever',
                'Lifetime access',
                'Priority support',
                'All future features'
            ]
        },
        'monthly': {
            'price': '$1.99',
            'price_id': Config.STRIPE_MONTHLY_PRICE_ID,
            'name': 'Monthly Premium',
            'description': 'Billed monthly',
            'features': [
                'No ads',
                'Cancel anytime',
                'Priority support'
            ]
        },
        'yearly': {
            'price': '$14.99',
            'price_id': Config.STRIPE_YEARLY_PRICE_ID,
            'name': 'Yearly Premium',
            'description': 'Save 37%',
            'features': [
                'No ads',
                'Best value',
                'Priority support',
                'All future features'
            ]
        }
    }
