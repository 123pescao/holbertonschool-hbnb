#!/usr/bin/python3
"""Entry Point"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
