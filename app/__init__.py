from flask import Flask
from app.config import Config
from app.extensions import jwt
from app.blueprints.auth import auth_bp
from app.blueprints.wallet import wallet_bp
from app.blueprints.dashboard import dashboard_bp
from app.blueprints.monitoring import monitoring_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(wallet_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(monitoring_bp)

    return app
