#!/usr/bin/python3
"""A script that starts a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """display hello message"""
    return "Hello HBNB!"


if __name__ == '__main__':
    # Run Flask app, listening on all available network interfaces on port 5000
    app.run(host='0.0.0.0', port=5000)
