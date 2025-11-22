from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Location, Warehouse

locations_bp = Blueprint('locations', __name__)

@locations_bp.route('', methods=['GET'])
@jwt_required()
def get_locations():
    warehouse_id = request.args.get('warehouse_id', type=int)
    query = Location.query
    
    if warehouse_id:
        query = query.filter_by(warehouse_id=warehouse_id)
    
    locations = query.all()
    return jsonify([l.to_dict() for l in locations]), 200

@locations_bp.route('', methods=['POST'])
@jwt_required()
def create_location():
    data = request.get_json()
    
    name = data.get('name', '').strip()
    short_code = data.get('short_code', '').strip().upper()
    warehouse_id = data.get('warehouse_id')
    
    if not name or not short_code or not warehouse_id:
        return jsonify({'error': 'Name, short code, and warehouse are required'}), 400
    
    warehouse = Warehouse.query.get(warehouse_id)
    if not warehouse:
        return jsonify({'error': 'Warehouse not found'}), 404
    
    if Location.query.filter_by(short_code=short_code, warehouse_id=warehouse_id).first():
        return jsonify({'error': 'Location with this short code already exists in this warehouse'}), 400
    
    location = Location(name=name, short_code=short_code, warehouse_id=warehouse_id)
    
    try:
        db.session.add(location)
        db.session.commit()
        return jsonify(location.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create location'}), 500

@locations_bp.route('/<int:location_id>', methods=['GET'])
@jwt_required()
def get_location(location_id):
    location = Location.query.get_or_404(location_id)
    return jsonify(location.to_dict()), 200

@locations_bp.route('/<int:location_id>', methods=['PUT'])
@jwt_required()
def update_location(location_id):
    location = Location.query.get_or_404(location_id)
    data = request.get_json()
    
    name = data.get('name', '').strip()
    short_code = data.get('short_code', '').strip().upper()
    warehouse_id = data.get('warehouse_id')
    
    if not name or not short_code or not warehouse_id:
        return jsonify({'error': 'Name, short code, and warehouse are required'}), 400
    
    if warehouse_id != location.warehouse_id or short_code != location.short_code:
        if Location.query.filter_by(short_code=short_code, warehouse_id=warehouse_id).first():
            return jsonify({'error': 'Location with this short code already exists in this warehouse'}), 400
    
    location.name = name
    location.short_code = short_code
    location.warehouse_id = warehouse_id
    
    try:
        db.session.commit()
        return jsonify(location.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update location'}), 500

@locations_bp.route('/<int:location_id>', methods=['DELETE'])
@jwt_required()
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    try:
        db.session.delete(location)
        db.session.commit()
        return jsonify({'message': 'Location deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete location'}), 500

