from flask import Flask
from .config import Config
from .extensions import jwt
from .auth import auth_bp
from .wallet import wallet_bp
from .dashboard import dashboard_bp
from .monitoring import monitoring_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(wallet_bp, url_prefix='/wallet')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(monitoring_bp, url_prefix='/monitoring')

    return app
