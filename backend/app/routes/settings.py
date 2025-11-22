from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from app import db
from app.models.warehouse import Warehouse
from app.models.location import Location

settings_bp = Blueprint('settings', __name__)
settings_ns = Namespace('settings', description='Settings management')

warehouse_model = settings_ns.model('Warehouse', {
    'name': fields.String(required=True),
    'short_code': fields.String(required=True),
    'address': fields.String()
})

location_model = settings_ns.model('Location', {
    'name': fields.String(required=True),
    'short_code': fields.String(required=True),
    'warehouse_short_code': fields.String(required=True)
})


@settings_bp.route('/warehouses', methods=['GET'])
@jwt_required()
def get_warehouses():
    """Get all warehouses"""
    warehouses = Warehouse.query.filter_by(is_active=True).all()
    return jsonify([w.to_dict() for w in warehouses]), 200


@settings_bp.route('/warehouses', methods=['POST'])
@jwt_required()
def create_warehouse():
    """Create a new warehouse"""
    data = request.get_json()
    
    if Warehouse.query.filter_by(short_code=data.get('short_code')).first():
        return jsonify({'error': 'Short code already exists'}), 400
    
    warehouse = Warehouse(
        name=data.get('name'),
        short_code=data.get('short_code'),
        address=data.get('address')
    )
    
    db.session.add(warehouse)
    db.session.commit()
    
    return jsonify(warehouse.to_dict()), 201


@settings_bp.route('/warehouses/<int:warehouse_id>', methods=['GET'])
@jwt_required()
def get_warehouse(warehouse_id):
    """Get warehouse details"""
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    return jsonify(warehouse.to_dict()), 200


@settings_bp.route('/warehouses/<int:warehouse_id>', methods=['PUT'])
@jwt_required()
def update_warehouse(warehouse_id):
    """Update warehouse"""
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    data = request.get_json()
    
    if data.get('short_code') and data.get('short_code') != warehouse.short_code:
        if Warehouse.query.filter_by(short_code=data.get('short_code')).first():
            return jsonify({'error': 'Short code already exists'}), 400
        warehouse.short_code = data.get('short_code')
    
    if data.get('name'):
        warehouse.name = data.get('name')
    
    if 'address' in data:
        warehouse.address = data.get('address')
    
    db.session.commit()
    
    return jsonify(warehouse.to_dict()), 200


@settings_bp.route('/warehouses/<int:warehouse_id>', methods=['DELETE'])
@jwt_required()
def delete_warehouse(warehouse_id):
    """Delete warehouse (soft delete)"""
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    warehouse.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Warehouse deleted'}), 200


@settings_bp.route('/locations', methods=['GET'])
@jwt_required()
def get_locations():
    """Get all locations"""
    warehouse_short_code = request.args.get('warehouse_short_code')
    
    query = Location.query.filter_by(is_active=True)
    
    if warehouse_short_code:
        warehouse = Warehouse.query.filter_by(short_code=warehouse_short_code).first()
        if warehouse:
            query = query.filter_by(warehouse_id=warehouse.id)
    
    locations = query.all()
    return jsonify([l.to_dict() for l in locations]), 200


@settings_bp.route('/locations', methods=['POST'])
@jwt_required()
def create_location():
    """Create a new location"""
    data = request.get_json()
    
    warehouse = Warehouse.query.filter_by(short_code=data.get('warehouse_short_code')).first()
    if not warehouse:
        return jsonify({'error': 'Warehouse not found'}), 404
    
    # Check if location with same short_code exists in this warehouse
    if Location.query.filter_by(
        warehouse_id=warehouse.id,
        short_code=data.get('short_code')
    ).first():
        return jsonify({'error': 'Location with this short code already exists in this warehouse'}), 400
    
    location = Location(
        name=data.get('name'),
        short_code=data.get('short_code'),
        warehouse_id=warehouse.id
    )
    
    db.session.add(location)
    db.session.commit()
    
    return jsonify(location.to_dict()), 201


@settings_bp.route('/locations/<int:location_id>', methods=['GET'])
@jwt_required()
def get_location(location_id):
    """Get location details"""
    location = Location.query.get_or_404(location_id)
    return jsonify(location.to_dict()), 200


@settings_bp.route('/locations/<int:location_id>', methods=['PUT'])
@jwt_required()
def update_location(location_id):
    """Update location"""
    location = Location.query.get_or_404(location_id)
    data = request.get_json()
    
    if data.get('name'):
        location.name = data.get('name')
    
    if data.get('short_code') and data.get('short_code') != location.short_code:
        if Location.query.filter_by(
            warehouse_id=location.warehouse_id,
            short_code=data.get('short_code')
        ).first():
            return jsonify({'error': 'Short code already exists in this warehouse'}), 400
        location.short_code = data.get('short_code')
    
    db.session.commit()
    
    return jsonify(location.to_dict()), 200


@settings_bp.route('/locations/<int:location_id>', methods=['DELETE'])
@jwt_required()
def delete_location(location_id):
    """Delete location (soft delete)"""
    location = Location.query.get_or_404(location_id)
    location.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Location deleted'}), 200


# RESTX Resources
@settings_ns.route('/warehouses')
class Warehouses(Resource):
    @jwt_required()
    @settings_ns.doc('get_warehouses')
    def get(self):
        return get_warehouses()
    
    @jwt_required()
    @settings_ns.expect(warehouse_model)
    @settings_ns.doc('create_warehouse')
    def post(self):
        return create_warehouse()


@settings_ns.route('/warehouses/<int:warehouse_id>')
class WarehouseDetail(Resource):
    @jwt_required()
    @settings_ns.doc('get_warehouse')
    def get(self, warehouse_id):
        return get_warehouse(warehouse_id)
    
    @jwt_required()
    @settings_ns.expect(warehouse_model)
    @settings_ns.doc('update_warehouse')
    def put(self, warehouse_id):
        return update_warehouse(warehouse_id)
    
    @jwt_required()
    @settings_ns.doc('delete_warehouse')
    def delete(self, warehouse_id):
        return delete_warehouse(warehouse_id)


@settings_ns.route('/locations')
class Locations(Resource):
    @jwt_required()
    @settings_ns.doc('get_locations')
    def get(self):
        return get_locations()
    
    @jwt_required()
    @settings_ns.expect(location_model)
    @settings_ns.doc('create_location')
    def post(self):
        return create_location()


@settings_ns.route('/locations/<int:location_id>')
class LocationDetail(Resource):
    @jwt_required()
    @settings_ns.doc('get_location')
    def get(self, location_id):
        return get_location(location_id)
    
    @jwt_required()
    @settings_ns.expect(location_model)
    @settings_ns.doc('update_location')
    def put(self, location_id):
        return update_location(location_id)
    
    @jwt_required()
    @settings_ns.doc('delete_location')
    def delete(self, location_id):
        return delete_location(location_id)

