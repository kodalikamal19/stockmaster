from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_restx import Namespace, Resource, fields
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app import db, limiter
from app.models.user import User
from app.validators import validate_login_id, validate_email, validate_password, ValidationError
from app.utils.otp_service import OTPService
from app.utils.email_service import EmailService

auth_bp = Blueprint('auth', __name__)
auth_ns = Namespace('auth', description='Authentication operations')

# Request models for Swagger
signup_model = auth_ns.model('Signup', {
    'login_id': fields.String(required=True, description='Login ID (6-12 characters)'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password'),
    'confirm_password': fields.String(required=True, description='Confirm password')
})

login_model = auth_ns.model('Login', {
    'login_id': fields.String(required=True, description='Login ID'),
    'password': fields.String(required=True, description='Password')
})

forgot_password_model = auth_ns.model('ForgotPassword', {
    'email': fields.String(required=True, description='Email address')
})

verify_otp_model = auth_ns.model('VerifyOTP', {
    'email': fields.String(required=True, description='Email address'),
    'otp': fields.String(required=True, description='OTP code')
})

reset_password_model = auth_ns.model('ResetPassword', {
    'email': fields.String(required=True, description='Email address'),
    'otp': fields.String(required=True, description='OTP code'),
    'new_password': fields.String(required=True, description='New password'),
    'confirm_password': fields.String(required=True, description='Confirm new password')
})


@auth_bp.route('/signup', methods=['POST'])
@limiter.limit("5 per minute")
def signup():
    """User signup"""
    data = request.get_json()
    
    try:
        # Validate inputs
        validate_login_id(data.get('login_id'))
        validate_email(data.get('email'))
        validate_password(data.get('password'))
        
        if data.get('password') != data.get('confirm_password'):
            return jsonify({'error': 'Passwords do not match'}), 400
        
        # Check if user exists
        if User.query.filter_by(login_id=data['login_id']).first():
            return jsonify({'error': 'Login ID already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create user
        user = User(
            login_id=data['login_id'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """User login"""
    data = request.get_json()
    
    login_id = data.get('login_id')
    password = data.get('password')
    
    if not login_id or not password:
        return jsonify({'error': 'Login ID and password are required'}), 400
    
    user = User.query.filter_by(login_id=login_id).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid login credentials'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is inactive'}), 403
    
    # Create tokens
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
    """Refresh access token"""
    current_user_id = get_jwt_identity()
    new_token = create_access_token(identity=current_user_id)
    return jsonify({'access_token': new_token}), 200


@auth_bp.route('/forgot-password', methods=['POST'])
@limiter.limit("3 per minute")
def forgot_password():
    """Send OTP for password reset"""
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        # Don't reveal if email exists for security
        return jsonify({'message': 'If the email exists, an OTP has been sent'}), 200
    
    # Generate and send OTP
    otp = OTPService.generate_otp(email)
    if otp:
        EmailService.send_otp_email(email, otp)
        return jsonify({'message': 'OTP sent to email'}), 200
    else:
        return jsonify({'error': 'Failed to generate OTP'}), 500


@auth_bp.route('/verify-otp', methods=['POST'])
@limiter.limit("10 per minute")
def verify_otp():
    """Verify OTP"""
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    
    if not email or not otp:
        return jsonify({'error': 'Email and OTP are required'}), 400
    
    if OTPService.verify_otp(email, otp):
        return jsonify({'message': 'OTP verified successfully'}), 200
    else:
        return jsonify({'error': 'Invalid or expired OTP'}), 400


@auth_bp.route('/reset-password', methods=['POST'])
@limiter.limit("5 per minute")
def reset_password():
    """Reset password with OTP"""
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    
    if not all([email, otp, new_password, confirm_password]):
        return jsonify({'error': 'All fields are required'}), 400
    
    if new_password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    try:
        validate_password(new_password)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    
    # Verify OTP
    if not OTPService.verify_otp(email, otp):
        return jsonify({'error': 'Invalid or expired OTP'}), 400
    
    # Update password
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.set_password(new_password)
    db.session.commit()
    
    return jsonify({'message': 'Password reset successfully'}), 200


# RESTX Resources for Swagger
@auth_ns.route('/signup')
class Signup(Resource):
    @auth_ns.expect(signup_model)
    @auth_ns.doc('signup')
    def post(self):
        return signup()


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.doc('login')
    def post(self):
        return login()


@auth_ns.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    @auth_ns.doc('refresh_token')
    def post(self):
        return refresh()


@auth_ns.route('/forgot-password')
class ForgotPassword(Resource):
    @auth_ns.expect(forgot_password_model)
    @auth_ns.doc('forgot_password')
    def post(self):
        return forgot_password()


@auth_ns.route('/verify-otp')
class VerifyOTP(Resource):
    @auth_ns.expect(verify_otp_model)
    @auth_ns.doc('verify_otp')
    def post(self):
        return verify_otp()


@auth_ns.route('/reset-password')
class ResetPassword(Resource):
    @auth_ns.expect(reset_password_model)
    @auth_ns.doc('reset_password')
    def post(self):
        return reset_password()

