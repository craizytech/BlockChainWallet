from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config
from app.extensions import jwt
from app.auth import auth_bp
from app.dashboard import dashboard_bp
from app.monitoring import monitoring_bp
from app.transactions import transactions_bp

def create_app():
    app = Flask(__name__)

    # Enable CORS with detailed settings
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    app.config.from_object(Config)

    # Initialize JWT
    jwt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(monitoring_bp, url_prefix='/monitoring')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')

    return app
