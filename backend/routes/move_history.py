from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, StockLedger, Location
from datetime import datetime
from sqlalchemy import or_, and_

move_history_bp = Blueprint('move_history', __name__)

@move_history_bp.route('', methods=['GET'])
@jwt_required()
def get_move_history():
    search = request.args.get('search', '').strip()
    warehouse_id = request.args.get('warehouse_id', type=int)
    product_id = request.args.get('product_id', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    operation_type = request.args.get('operation_type')
    
    query = StockLedger.query
    
    if search:
        query = query.filter(
            or_(
                StockLedger.reference.ilike(f'%{search}%'),
                StockLedger.contact.ilike(f'%{search}%')
            )
        )
    
    if warehouse_id:
        # Filter by warehouse - get location IDs for this warehouse
        location_ids = [loc.id for loc in Location.query.filter_by(warehouse_id=warehouse_id).all()]
        if location_ids:
            query = query.filter(
                or_(
                    StockLedger.from_location_id.in_(location_ids),
                    StockLedger.to_location_id.in_(location_ids)
                )
            )
        else:
            # No locations in this warehouse, return empty
            return jsonify([]), 200
    
    if product_id:
        query = query.filter_by(product_id=product_id)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(StockLedger.date >= date_from_obj)
        except:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(StockLedger.date <= date_to_obj)
        except:
            pass
    
    if operation_type:
        query = query.filter_by(operation_type=operation_type)
    
    # Sorting
    sort_by = request.args.get('sort_by', 'date')
    sort_order = request.args.get('sort_order', 'desc')
    
    if sort_by == 'date':
        if sort_order == 'desc':
            query = query.order_by(StockLedger.date.desc())
        else:
            query = query.order_by(StockLedger.date.asc())
    elif sort_by == 'reference':
        if sort_order == 'desc':
            query = query.order_by(StockLedger.reference.desc())
        else:
            query = query.order_by(StockLedger.reference.asc())
    else:
        query = query.order_by(StockLedger.date.desc())
    
    history = query.all()
    return jsonify([h.to_dict() for h in history]), 200

