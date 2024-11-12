#!/usr/bin/python3
"""Entry Point"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

from app import create_app
from app.extensions import db, migrate
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run()
