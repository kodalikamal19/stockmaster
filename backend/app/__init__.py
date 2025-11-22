from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_restx import Api
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
mail = Mail()
api = Api(
    title='StockMaster API',
    version='1.0',
    description='Warehouse Management System API',
    doc='/api/docs'
)


def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'postgresql://stockmaster:stockmaster123@localhost:5432/stockmaster'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 2592000))
    
    # Mail configuration
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    
    # OTP configuration
    app.config['OTP_SECRET_KEY'] = os.environ.get('OTP_SECRET_KEY', 'otp-secret-key')
    app.config['OTP_VALIDITY_MINUTES'] = 10
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)
    
    # CORS configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(','),
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    from app.routes import auth_bp, operations_bp, stock_bp, history_bp, settings_bp, profile_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(operations_bp, url_prefix='/api/operations')
    app.register_blueprint(stock_bp, url_prefix='/api/stock')
    app.register_blueprint(history_bp, url_prefix='/api/history')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    
    # Register API namespaces
    from app.routes import auth_ns, operations_ns, stock_ns, history_ns, settings_ns, profile_ns
    api.init_app(app)
    api.add_namespace(auth_ns)
    api.add_namespace(operations_ns)
    api.add_namespace(stock_ns)
    api.add_namespace(history_ns)
    api.add_namespace(settings_ns)
    api.add_namespace(profile_ns)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

