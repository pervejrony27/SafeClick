"""
============================================
APP.PY — Flask Application Factory
Creates and configures the Flask app
============================================
"""

from flask import Flask
from flask_cors import CORS
from api.routes import scanner_bp


def create_app():
    """Create and configure the Flask application"""

    # Create Flask app
    app = Flask(__name__)

    # ── CORS Configuration ──
    # This allows the frontend (different port) to call our API
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5500",      # VS Code Live Server
                "http://127.0.0.1:5500",      # Alternative localhost
                "http://localhost:3000",       # React (if used later)
                "http://127.0.0.1:5500",
                "null",                       # For file:// protocol
            ],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        }
    })

    # ── Register Blueprints (Routes) ──
    app.register_blueprint(scanner_bp)

    # ── Health Check Route ──
    @app.route("/")
    def health_check():
        return {
            "status": "running",
            "message": " SafeClick  API is running!",
            "endpoints": {
                "scan": "POST /api/scan",
                "health": "GET /api/health",
            }
        }

    return app