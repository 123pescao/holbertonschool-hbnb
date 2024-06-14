#!/usr/bin/python3
from flask import Flask
app = Flask(__name__)

# Example route for testing
@app.route('/')
def index():
    return "Welcome to HBnB API"

if __name__ == '__main__':
    app.run(debug=True)