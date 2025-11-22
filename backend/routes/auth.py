from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from models import db, User, OTP
from datetime import datetime, timedelta
import re
import random
import smtplib
from email.mime.text import MIMEText
from config import Config

auth_bp = Blueprint('auth', __name__)

def validate_password(password):
    """Validate password: >= 8 chars, uppercase + lowercase + digit + special char"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, "Valid"

def send_otp_email(email, otp_code):
    """Send OTP email"""
    try:
        msg = MIMEText(f'Your StockMaster password reset OTP is: {otp_code}\n\nThis OTP will expire in 10 minutes.')
        msg['Subject'] = 'StockMaster Password Reset OTP'
        msg['From'] = Config.MAIL_USERNAME
        msg['To'] = email
        
        server = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
        server.starttls()
        server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    login_id = data.get('login_id', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')
    
    # Validations
    if not login_id or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    
    if len(login_id) < 6 or len(login_id) > 12:
        return jsonify({'error': 'Login ID must be between 6 and 12 characters'}), 400
    
    if User.query.filter_by(login_id=login_id).first():
        return jsonify({'error': 'Login ID already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    is_valid, message = validate_password(password)
    if not is_valid:
        return jsonify({'error': message}), 400
    
    # Create user
    user = User(login_id=login_id, email=email)
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create user'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    login_id = data.get('login_id', '').strip()
    password = data.get('password', '')
    
    if not login_id or not password:
        return jsonify({'error': 'Login ID and password are required'}), 400
    
    user = User.query.filter_by(login_id=login_id).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid login credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        # Don't reveal if email exists for security
        return jsonify({'message': 'If the email exists, an OTP has been sent'}), 200
    
    # Generate 6-digit OTP
    otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    expires_at = datetime.utcnow() + timedelta(minutes=Config.OTP_EXPIRY_MINUTES)
    
    # Invalidate old OTPs
    OTP.query.filter_by(email=email, used=False).update({'used': True})
    
    # Create new OTP
    otp = OTP(email=email, otp_code=otp_code, expires_at=expires_at)
    db.session.add(otp)
    db.session.commit()
    
    # Send email
    if send_otp_email(email, otp_code):
        return jsonify({'message': 'OTP sent to your email'}), 200
    else:
        return jsonify({'error': 'Failed to send OTP email'}), 500

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    otp_code = data.get('otp', '').strip()
    
    if not email or not otp_code:
        return jsonify({'error': 'Email and OTP are required'}), 400
    
    otp = OTP.query.filter_by(email=email, otp_code=otp_code, used=False).first()
    
    if not otp:
        return jsonify({'error': 'Invalid OTP'}), 400
    
    if datetime.utcnow() > otp.expires_at:
        return jsonify({'error': 'OTP has expired'}), 400
    
    # Mark OTP as used
    otp.used = True
    db.session.commit()
    
    return jsonify({'message': 'OTP verified successfully'}), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    otp_code = data.get('otp', '').strip()
    new_password = data.get('new_password', '')
    
    if not email or not otp_code or not new_password:
        return jsonify({'error': 'All fields are required'}), 400
    
    # Verify OTP
    otp = OTP.query.filter_by(email=email, otp_code=otp_code, used=False).first()
    
    if not otp:
        return jsonify({'error': 'Invalid or expired OTP'}), 400
    
    if datetime.utcnow() > otp.expires_at:
        return jsonify({'error': 'OTP has expired'}), 400
    
    # Validate password
    is_valid, message = validate_password(new_password)
    if not is_valid:
        return jsonify({'error': message}), 400
    
    # Update password
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.set_password(new_password)
    otp.used = True
    db.session.commit()
    
    return jsonify({'message': 'Password reset successfully'}), 200

