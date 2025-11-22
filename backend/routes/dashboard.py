from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Operation
from datetime import date, datetime
from sqlalchemy import func, and_, or_

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    today = date.today()
    
    # Receipts stats
    receipts_pending = Operation.query.filter_by(
        operation_type='IN',
        status='pending'
    ).count()
    
    receipts_scheduled = Operation.query.filter(
        Operation.operation_type == 'IN',
        Operation.status == 'pending',
        Operation.schedule_date > today
    ).count()
    
    receipts_late = Operation.query.filter(
        Operation.operation_type == 'IN',
        Operation.status == 'pending',
        Operation.schedule_date < today
    ).count()
    
    # Check for receipts waiting for stock (simplified - can be enhanced)
    receipts_waiting = 0  # Placeholder - can be enhanced based on business logic
    
    # Deliveries stats
    deliveries_pending = Operation.query.filter_by(
        operation_type='OUT',
        status='pending'
    ).count()
    
    deliveries_scheduled = Operation.query.filter(
        Operation.operation_type == 'OUT',
        Operation.status == 'pending',
        Operation.schedule_date > today
    ).count()
    
    deliveries_late = Operation.query.filter(
        Operation.operation_type == 'OUT',
        Operation.status == 'pending',
        Operation.schedule_date < today
    ).count()
    
    # Check for deliveries waiting for stock (insufficient stock)
    deliveries_waiting = 0  # Placeholder - can be enhanced based on stock availability
    
    return jsonify({
        'receipts': {
            'pending': receipts_pending,
            'scheduled': receipts_scheduled,
            'late': receipts_late,
            'waiting_for_stock': receipts_waiting
        },
        'deliveries': {
            'pending': deliveries_pending,
            'scheduled': deliveries_scheduled,
            'late': deliveries_late,
            'waiting_for_stock': deliveries_waiting
        }
    }), 200

