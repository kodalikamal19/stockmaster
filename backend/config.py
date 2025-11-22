import os
from datetime import timedelta

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Kamal20*@localhost:5432/stockmaster1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Email SMTP
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kodalikamal1908@gmail.com'
    MAIL_PASSWORD = 'pyxk auii kwsr dhbz'
    
    # OTP
    OTP_EXPIRY_MINUTES = 10

