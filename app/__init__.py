from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Register blueprints
    from app.auth.routes import auth_bp
    from app.wallet.routes import wallet_bp
    from app.dashboard.routes import dashboard_bp
    from app.monitoring.routes import monitoring_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(wallet_bp, url_prefix='/wallet')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(monitoring_bp, url_prefix='/monitoring')
    
    return app
