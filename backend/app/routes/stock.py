from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from app import db
from app.models.stock_level import StockLevel
from app.models.product import Product
from app.models.location import Location
from sqlalchemy import or_, and_

stock_bp = Blueprint('stock', __name__)
stock_ns = Namespace('stock', description='Stock management')


@stock_bp.route('', methods=['GET'])
@jwt_required()
def get_stock():
    """Get all stock with search, filters, sorting, and pagination"""
    search = request.args.get('search', '')
    product_id = request.args.get('product_id', type=int)
    location_id = request.args.get('location_id', type=int)
    low_stock = request.args.get('low_stock', type=bool)
    sort_by = request.args.get('sort_by', 'product.name')
    sort_order = request.args.get('sort_order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = db.session.query(StockLevel).join(Product).join(Location)
    
    # Search filter
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f'%{search}%'),
                Product.sku.ilike(f'%{search}%')
            )
        )
    
    # Product filter
    if product_id:
        query = query.filter(StockLevel.product_id == product_id)
    
    # Location filter
    if location_id:
        query = query.filter(StockLevel.location_id == location_id)
    
    # Low stock filter
    if low_stock:
        query = query.filter(StockLevel.quantity_on_hand < 10)
    
    # Sorting
    if sort_by == 'product.name':
        order_col = Product.name
    elif sort_by == 'sku':
        order_col = Product.sku
    elif sort_by == 'quantity_on_hand':
        order_col = StockLevel.quantity_on_hand
    elif sort_by == 'unit_cost':
        order_col = Product.unit_cost
    else:
        order_col = StockLevel.updated_at
    
    if sort_order == 'desc':
        query = query.order_by(order_col.desc())
    else:
        query = query.order_by(order_col.asc())
    
    # Pagination
    stock_items = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [item.to_dict() for item in stock_items.items],
        'total': stock_items.total,
        'page': page,
        'per_page': per_page,
        'pages': stock_items.pages
    }), 200


@stock_bp.route('/<int:product_id>/<int:location_id>', methods=['GET'])
@jwt_required()
def get_stock_level(product_id, location_id):
    """Get stock level for a specific product and location"""
    from app.services.stock_service import StockService
    stock = StockService.get_stock_level(product_id, location_id)
    return jsonify(stock), 200


@stock_bp.route('/<int:product_id>/<int:location_id>/ledger', methods=['GET'])
@jwt_required()
def get_stock_ledger(product_id, location_id):
    """Get ledger entries for a product at a location"""
    from app.models.stock_ledger import StockLedger
    from datetime import datetime
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = StockLedger.query.filter_by(
        product_id=product_id,
        location_id=location_id
    )
    
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            query = query.filter(StockLedger.created_at >= start)
        except:
            pass
    
    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            query = query.filter(StockLedger.created_at <= end)
        except:
            pass
    
    entries = query.order_by(StockLedger.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'items': [entry.to_dict() for entry in entries.items],
        'total': entries.total,
        'page': page,
        'per_page': per_page,
        'pages': entries.pages
    }), 200


# RESTX Resources
@stock_ns.route('')
class Stock(Resource):
    @jwt_required()
    @stock_ns.doc('get_stock')
    def get(self):
        return get_stock()


@stock_ns.route('/<int:product_id>/<int:location_id>')
class StockLevel(Resource):
    @jwt_required()
    @stock_ns.doc('get_stock_level')
    def get(self, product_id, location_id):
        return get_stock_level(product_id, location_id)


@stock_ns.route('/<int:product_id>/<int:location_id>/ledger')
class StockLedger(Resource):
    @jwt_required()
    @stock_ns.doc('get_stock_ledger')
    def get(self, product_id, location_id):
        return get_stock_ledger(product_id, location_id)

