import os

from flask import Flask
from flask_cors import CORS

from api import api_bp
from logger_config import logger

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Enable CORS for specific routes
# CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(api_bp)

if not os.path.exists("credentials.json"):
    logger.error("credentials.json file not found.")
    logger.error("Please download the credentials.json file from Google Cloud Console.")
    logger.error("Place the file in the backend/src directory.")
    logger.error("Refer to the README.md file for more information.")
    exit(1)

if __name__ == "__main__":
    app.run(debug=True)
