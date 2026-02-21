# PDF Inverter WSGI Configuration
# This file is used for shared hosting deployment (e.g., cPanel with Python support)

import sys
import os

# Add your project directory to the sys.path
project_home = os.path.dirname(__file__)
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import the Flask application
from app import app as application

# This is what the WSGI server will use
if __name__ == "__main__":
    application.run()
