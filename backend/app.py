import os
import sys

from flask import Flask
from flask_cors import CORS

from src.api import api_blueprint
from src.logger_config import logger

app = Flask(__name__)

# Allow all origins, methods, and headers
CORS(app, resources={r'/api/*': {'origins': '*'}}, supports_credentials=True)

# OR (If you want to allow only specific frontend URL)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

app.register_blueprint(api_blueprint)

if not os.path.exists('creds/credentials.json'):
    logger.error('credentials.json file not found.')
    logger.error('Please download the credentials.json file from Google Cloud Console.')
    logger.error('Place the file in the backend/src directory.')
    logger.error('Refer to the README.md file for more information.')
    sys.exit(1)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
