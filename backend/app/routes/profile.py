from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource
from app import db
from app.models.user import User

profile_bp = Blueprint('profile', __name__)
profile_ns = Namespace('profile', description='Profile management')


@profile_bp.route('', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200


@profile_bp.route('', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user profile"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if data.get('first_name'):
        user.first_name = data.get('first_name')
    
    if data.get('last_name'):
        user.last_name = data.get('last_name')
    
    if data.get('email') and data.get('email') != user.email:
        # Check if email already exists
        if User.query.filter_by(email=data.get('email')).first():
            return jsonify({'error': 'Email already exists'}), 400
        user.email = data.get('email')
    
    db.session.commit()
    
    return jsonify(user.to_dict()), 200


@profile_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (client should discard tokens)"""
    # In a stateless JWT system, logout is handled client-side
    # But we can add token blacklisting here if needed
    return jsonify({'message': 'Logged out successfully'}), 200


# RESTX Resources
@profile_ns.route('')
class Profile(Resource):
    @jwt_required()
    @profile_ns.doc('get_profile')
    def get(self):
        return get_profile()
    
    @jwt_required()
    @profile_ns.doc('update_profile')
    def put(self):
        return update_profile()


@profile_ns.route('/logout')
class Logout(Resource):
    @jwt_required()
    @profile_ns.doc('logout')
    def post(self):
        return logout()

