#!/usr/bin/python3
"""Entry Point"""
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from flask_cors import CORS
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5500", "http://127.0.0.1:5500"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

if __name__ == '__main__':
    app.run(debug=True)
