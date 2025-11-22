from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, StockLevel, Product, Location
from sqlalchemy import or_

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('', methods=['GET'])
@jwt_required()
def get_stock():
    search = request.args.get('search', '').strip()
    warehouse_id = request.args.get('warehouse_id', type=int)
    location_id = request.args.get('location_id', type=int)
    product_id = request.args.get('product_id', type=int)
    
    query = db.session.query(StockLevel).join(Product).join(Location)
    
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f'%{search}%'),
                Product.sku.ilike(f'%{search}%')
            )
        )
    
    if warehouse_id:
        query = query.filter(Location.warehouse_id == warehouse_id)
    
    if location_id:
        query = query.filter(StockLevel.location_id == location_id)
    
    if product_id:
        query = query.filter(StockLevel.product_id == product_id)
    
    # Sorting
    sort_by = request.args.get('sort_by', 'product_name')
    sort_order = request.args.get('sort_order', 'asc')
    
    if sort_by == 'product_name':
        if sort_order == 'asc':
            query = query.order_by(Product.name.asc())
        else:
            query = query.order_by(Product.name.desc())
    elif sort_by == 'sku':
        if sort_order == 'asc':
            query = query.order_by(Product.sku.asc())
        else:
            query = query.order_by(Product.sku.desc())
    elif sort_by == 'qty_on_hand':
        if sort_order == 'asc':
            query = query.order_by(StockLevel.qty_on_hand.asc())
        else:
            query = query.order_by(StockLevel.qty_on_hand.desc())
    else:
        query = query.order_by(StockLevel.updated_at.desc())
    
    stock_levels = query.all()
    return jsonify([s.to_dict() for s in stock_levels]), 200

