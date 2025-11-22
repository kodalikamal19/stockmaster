"""
Script to insert a test user into the database
Run: python insert_test_user.py
"""
from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create test user
    login_id = 'admin001'
    email = 'admin@stockmaster.com'
    password = 'Password123!'  # Change this to your desired password
    
    # Check if user exists
    existing_user = User.query.filter_by(login_id=login_id).first()
    
    if existing_user:
        print(f"User {login_id} already exists!")
        print(f"Updating password...")
        existing_user.set_password(password)
        existing_user.email = email
    else:
        print(f"Creating user {login_id}...")
        user = User(login_id=login_id, email=email)
        user.set_password(password)
        db.session.add(user)
    
    try:
        db.session.commit()
        print(f"✓ User created/updated successfully!")
        print(f"  Login ID: {login_id}")
        print(f"  Email: {email}")
        print(f"  Password: {password}")
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error: {e}")

