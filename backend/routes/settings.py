from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from routes.warehouses import warehouses_bp
from routes.locations import locations_bp

settings_bp = Blueprint('settings', __name__)

# Settings routes delegate to warehouses and locations
@settings_bp.route('/warehouses', methods=['GET'])
@jwt_required()
def get_warehouses():
    from routes.warehouses import get_warehouses as wh_get
    return wh_get()

@settings_bp.route('/warehouses', methods=['POST'])
@jwt_required()
def create_warehouse():
    from routes.warehouses import create_warehouse as wh_create
    return wh_create()

@settings_bp.route('/warehouses/<int:warehouse_id>', methods=['PUT'])
@jwt_required()
def update_warehouse(warehouse_id):
    from routes.warehouses import update_warehouse as wh_update
    return wh_update(warehouse_id)

@settings_bp.route('/warehouses/<int:warehouse_id>', methods=['DELETE'])
@jwt_required()
def delete_warehouse(warehouse_id):
    from routes.warehouses import delete_warehouse as wh_delete
    return wh_delete(warehouse_id)

@settings_bp.route('/locations', methods=['GET'])
@jwt_required()
def get_locations():
    from routes.locations import get_locations as loc_get
    return loc_get()

@settings_bp.route('/locations', methods=['POST'])
@jwt_required()
def create_location():
    from routes.locations import create_location as loc_create
    return loc_create()

@settings_bp.route('/locations/<int:location_id>', methods=['PUT'])
@jwt_required()
def update_location(location_id):
    from routes.locations import update_location as loc_update
    return loc_update(location_id)

@settings_bp.route('/locations/<int:location_id>', methods=['DELETE'])
@jwt_required()
def delete_location(location_id):
    from routes.locations import delete_location as loc_delete
    return loc_delete(location_id)

