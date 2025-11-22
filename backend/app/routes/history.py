from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from app import db
from app.models.stock_ledger import StockLedger, LedgerType
from datetime import datetime
from sqlalchemy import or_, and_

history_bp = Blueprint('history', __name__)
history_ns = Namespace('history', description='Move history')


@history_bp.route('', methods=['GET'])
@jwt_required()
def get_move_history():
    """Get move history with filters"""
    search = request.args.get('search', '')
    from_location_id = request.args.get('from_location_id', type=int)
    to_location_id = request.args.get('to_location_id', type=int)
    ledger_type = request.args.get('ledger_type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = db.session.query(StockLedger).join(StockLedger.product)
    
    # Search filter
    if search:
        query = query.filter(
            or_(
                StockLedger.reference.ilike(f'%{search}%'),
                StockLedger.contact_name.ilike(f'%{search}%'),
                StockLedger.product.has(name=search)
            )
        )
    
    # Location filters
    if from_location_id:
        query = query.filter(StockLedger.from_location_id == from_location_id)
    
    if to_location_id:
        query = query.filter(StockLedger.to_location_id == to_location_id)
    
    # Both locations (transfer)
    if from_location_id and to_location_id:
        query = query.filter(
            and_(
                StockLedger.from_location_id == from_location_id,
                StockLedger.to_location_id == to_location_id
            )
        )
    
    # Ledger type filter
    if ledger_type:
        try:
            type_enum = LedgerType(ledger_type)
            query = query.filter(StockLedger.ledger_type == type_enum)
        except ValueError:
            pass
    
    # Date range filters
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
    
    # Sorting
    if sort_by == 'reference':
        order_col = StockLedger.reference
    elif sort_by == 'date':
        order_col = StockLedger.created_at
    elif sort_by == 'quantity':
        order_col = StockLedger.quantity
    else:
        order_col = StockLedger.created_at
    
    if sort_order == 'asc':
        query = query.order_by(order_col.asc())
    else:
        query = query.order_by(order_col.desc())
    
    # Pagination
    entries = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [entry.to_dict() for entry in entries.items],
        'total': entries.total,
        'page': page,
        'per_page': per_page,
        'pages': entries.pages
    }), 200


# RESTX Resources
@history_ns.route('')
class MoveHistory(Resource):
    @jwt_required()
    @history_ns.doc('get_move_history')
    def get(self):
        return get_move_history()

