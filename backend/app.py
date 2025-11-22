from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes.auth import auth_bp
from routes.warehouses import warehouses_bp
from routes.locations import locations_bp
from routes.products import products_bp
from routes.operations import operations_bp
from routes.stock import stock_bp
from routes.move_history import move_history_bp
from routes.dashboard import dashboard_bp
from routes.settings import settings_bp
from routes.profile import profile_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, supports_credentials=True)
    
    db.init_app(app)
    Migrate(app, db)
    
    # Initialize JWT Manager
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(warehouses_bp, url_prefix='/api/warehouses')
    app.register_blueprint(locations_bp, url_prefix='/api/locations')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(operations_bp, url_prefix='/api/operations')
    app.register_blueprint(stock_bp, url_prefix='/api/stock')
    app.register_blueprint(move_history_bp, url_prefix='/api/move-history')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)

