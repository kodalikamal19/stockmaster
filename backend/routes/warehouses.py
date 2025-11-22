from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Warehouse

warehouses_bp = Blueprint('warehouses', __name__)

@warehouses_bp.route('', methods=['GET'])
@jwt_required()
def get_warehouses():
    warehouses = Warehouse.query.all()
    return jsonify([w.to_dict() for w in warehouses]), 200

@warehouses_bp.route('', methods=['POST'])
@jwt_required()
def create_warehouse():
    data = request.get_json()
    
    name = data.get('name', '').strip()
    short_code = data.get('short_code', '').strip().upper()
    address = data.get('address', '').strip()
    
    if not name or not short_code:
        return jsonify({'error': 'Name and short code are required'}), 400
    
    if Warehouse.query.filter_by(short_code=short_code).first():
        return jsonify({'error': 'Short code already exists'}), 400
    
    warehouse = Warehouse(name=name, short_code=short_code, address=address)
    
    try:
        db.session.add(warehouse)
        db.session.commit()
        return jsonify(warehouse.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create warehouse'}), 500

@warehouses_bp.route('/<int:warehouse_id>', methods=['GET'])
@jwt_required()
def get_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    return jsonify(warehouse.to_dict()), 200

@warehouses_bp.route('/<int:warehouse_id>', methods=['PUT'])
@jwt_required()
def update_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    data = request.get_json()
    
    name = data.get('name', '').strip()
    short_code = data.get('short_code', '').strip().upper()
    address = data.get('address', '').strip()
    
    if not name or not short_code:
        return jsonify({'error': 'Name and short code are required'}), 400
    
    if short_code != warehouse.short_code:
        if Warehouse.query.filter_by(short_code=short_code).first():
            return jsonify({'error': 'Short code already exists'}), 400
    
    warehouse.name = name
    warehouse.short_code = short_code
    warehouse.address = address
    
    try:
        db.session.commit()
        return jsonify(warehouse.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update warehouse'}), 500

@warehouses_bp.route('/<int:warehouse_id>', methods=['DELETE'])
@jwt_required()
def delete_warehouse(warehouse_id):
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    
    try:
        db.session.delete(warehouse)
        db.session.commit()
        return jsonify({'message': 'Warehouse deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete warehouse'}), 500

