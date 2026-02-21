import sys
import os

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load env variables from .env if present (won't override Vercel env vars)
from dotenv import load_dotenv
load_dotenv()

from app import app

# Vercel expects this handler
handler = app
