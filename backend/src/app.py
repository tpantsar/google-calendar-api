from flask import Flask
from flask_cors import CORS

from api import api_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Enable CORS for specific routes
# CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(debug=True)
