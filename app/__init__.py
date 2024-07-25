from flask import Flask
from app.config import Config
from app.extensions import jwt
from app.auth import auth_bp
from app.wallet import wallet_bp
from app.dashboard import dashboard_bp
from app.monitoring import monitoring_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(wallet_bp, url_prefix='/wallet')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(monitoring_bp, url_prefix='/monitoring')

    return app
