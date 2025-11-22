from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Operation, OperationLine, StockLevel, Location, Warehouse, StockLedger, Product
from datetime import datetime, date
from sqlalchemy import func

operations_bp = Blueprint('operations', __name__)

def generate_reference(warehouse_short_code, operation_type):
    """Generate reference: <WarehouseShortCode>/<OperationType>/<AutoIncrementID>"""
    # Get the last operation for this warehouse and operation type
    prefix = f"{warehouse_short_code}/{operation_type}/"
    last_op = Operation.query.filter(
        Operation.reference.like(f"{prefix}%")
    ).order_by(Operation.id.desc()).first()
    
    if last_op:
        # Extract the number from the last reference
        try:
            last_num = int(last_op.reference.split('/')[-1])
            next_num = last_num + 1
        except:
            next_num = 1
    else:
        next_num = 1
    
    return f"{prefix}{next_num:04d}"

@operations_bp.route('/receipts', methods=['GET'])
@jwt_required()
def get_receipts():
    search = request.args.get('search', '').strip()
    query = Operation.query.filter_by(operation_type='IN')
    
    if search:
        query = query.filter(
            (Operation.reference.ilike(f'%{search}%')) |
            (Operation.contact.ilike(f'%{search}%'))
        )
    
    receipts = query.order_by(Operation.created_at.desc()).all()
    return jsonify([r.to_dict() for r in receipts]), 200

@operations_bp.route('/deliveries', methods=['GET'])
@jwt_required()
def get_deliveries():
    search = request.args.get('search', '').strip()
    query = Operation.query.filter_by(operation_type='OUT')
    
    if search:
        query = query.filter(
            (Operation.reference.ilike(f'%{search}%')) |
            (Operation.contact.ilike(f'%{search}%'))
        )
    
    deliveries = query.order_by(Operation.created_at.desc()).all()
    return jsonify([d.to_dict() for d in deliveries]), 200

@operations_bp.route('/adjustments', methods=['GET'])
@jwt_required()
def get_adjustments():
    search = request.args.get('search', '').strip()
    query = Operation.query.filter_by(operation_type='ADJ')
    
    if search:
        query = query.filter(
            (Operation.reference.ilike(f'%{search}%')) |
            (Operation.contact.ilike(f'%{search}%'))
        )
    
    adjustments = query.order_by(Operation.created_at.desc()).all()
    return jsonify([a.to_dict() for a in adjustments]), 200

@operations_bp.route('/receipts', methods=['POST'])
@jwt_required()
def create_receipt():
    data = request.get_json()
    
    to_location_id = data.get('to_location_id')
    contact = data.get('contact', '').strip()
    schedule_date_str = data.get('schedule_date')
    lines = data.get('lines', [])
    
    if not to_location_id or not lines:
        return jsonify({'error': 'To location and lines are required'}), 400
    
    to_location = Location.query.get(to_location_id)
    if not to_location:
        return jsonify({'error': 'To location not found'}), 404
    
    warehouse_short_code = to_location.warehouse.short_code
    reference = generate_reference(warehouse_short_code, 'IN')
    
    schedule_date = None
    if schedule_date_str:
        try:
            schedule_date = datetime.strptime(schedule_date_str, '%Y-%m-%d').date()
        except:
            pass
    
    operation = Operation(
        reference=reference,
        operation_type='IN',
        to_location_id=to_location_id,
        contact=contact,
        schedule_date=schedule_date,
        status='pending'
    )
    
    try:
        db.session.add(operation)
        db.session.flush()
        
        for line_data in lines:
            product_id = line_data.get('product_id')
            quantity = line_data.get('quantity', 0)
            unit_cost = line_data.get('unit_cost', 0)
            
            if not product_id:
                continue
            
            line = OperationLine(
                operation_id=operation.id,
                product_id=product_id,
                quantity=quantity,
                unit_cost=unit_cost
            )
            db.session.add(line)
        
        db.session.commit()
        return jsonify(operation.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create receipt: {str(e)}'}), 500

@operations_bp.route('/deliveries', methods=['POST'])
@jwt_required()
def create_delivery():
    data = request.get_json()
    
    from_location_id = data.get('from_location_id')
    contact = data.get('contact', '').strip()
    schedule_date_str = data.get('schedule_date')
    lines = data.get('lines', [])
    
    if not from_location_id or not lines:
        return jsonify({'error': 'From location and lines are required'}), 400
    
    from_location = Location.query.get(from_location_id)
    if not from_location:
        return jsonify({'error': 'From location not found'}), 404
    
    warehouse_short_code = from_location.warehouse.short_code
    reference = generate_reference(warehouse_short_code, 'OUT')
    
    schedule_date = None
    if schedule_date_str:
        try:
            schedule_date = datetime.strptime(schedule_date_str, '%Y-%m-%d').date()
        except:
            pass
    
    operation = Operation(
        reference=reference,
        operation_type='OUT',
        from_location_id=from_location_id,
        contact=contact,
        schedule_date=schedule_date,
        status='pending'
    )
    
    try:
        db.session.add(operation)
        db.session.flush()
        
        for line_data in lines:
            product_id = line_data.get('product_id')
            quantity = line_data.get('quantity', 0)
            unit_cost = line_data.get('unit_cost', 0)
            
            if not product_id:
                continue
            
            line = OperationLine(
                operation_id=operation.id,
                product_id=product_id,
                quantity=quantity,
                unit_cost=unit_cost
            )
            db.session.add(line)
        
        db.session.commit()
        return jsonify(operation.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create delivery: {str(e)}'}), 500

@operations_bp.route('/adjustments', methods=['POST'])
@jwt_required()
def create_adjustment():
    data = request.get_json()
    
    location_id = data.get('location_id')
    product_id = data.get('product_id')
    counted_quantity = data.get('counted_quantity', 0)
    contact = data.get('contact', '').strip()
    
    if not location_id or not product_id:
        return jsonify({'error': 'Location and product are required'}), 400
    
    location = Location.query.get(location_id)
    if not location:
        return jsonify({'error': 'Location not found'}), 404
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    warehouse_short_code = location.warehouse.short_code
    reference = generate_reference(warehouse_short_code, 'ADJ')
    
    # Get current stock
    stock = StockLevel.query.filter_by(
        product_id=product_id,
        location_id=location_id
    ).first()
    
    current_qty = float(stock.qty_on_hand) if stock else 0.0
    adjustment_qty = counted_quantity - current_qty
    
    operation = Operation(
        reference=reference,
        operation_type='ADJ',
        to_location_id=location_id,
        contact=contact,
        status='pending'
    )
    
    try:
        db.session.add(operation)
        db.session.flush()
        
        line = OperationLine(
            operation_id=operation.id,
            product_id=product_id,
            quantity=abs(adjustment_qty),
            unit_cost=product.unit_cost or 0
        )
        db.session.add(line)
        
        # Update stock immediately for adjustments
        if not stock:
            stock = StockLevel(
                product_id=product_id,
                location_id=location_id,
                qty_on_hand=counted_quantity,
                free_to_use=counted_quantity
            )
            db.session.add(stock)
        else:
            stock.qty_on_hand = counted_quantity
            stock.free_to_use = counted_quantity
        
        # Create ledger entry
        ledger = StockLedger(
            reference=reference,
            product_id=product_id,
            to_location_id=location_id,
            quantity=adjustment_qty,
            operation_type='ADJ',
            status='validated',
            contact=contact
        )
        db.session.add(ledger)
        
        operation.status = 'validated'
        operation.validated_at = datetime.utcnow()
        
        db.session.commit()
        return jsonify(operation.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create adjustment: {str(e)}'}), 500

@operations_bp.route('/<int:operation_id>', methods=['GET'])
@jwt_required()
def get_operation(operation_id):
    operation = Operation.query.get_or_404(operation_id)
    return jsonify(operation.to_dict()), 200

@operations_bp.route('/<int:operation_id>/validate', methods=['POST'])
@jwt_required()
def validate_operation(operation_id):
    operation = Operation.query.get_or_404(operation_id)
    
    if operation.status != 'pending':
        return jsonify({'error': 'Operation is not pending'}), 400
    
    try:
        for line in operation.lines:
            product_id = line.product_id
            quantity = float(line.quantity)
            
            if operation.operation_type == 'IN':
                # Increase stock at to_location
                location_id = operation.to_location_id
                stock = StockLevel.query.filter_by(
                    product_id=product_id,
                    location_id=location_id
                ).first()
                
                if not stock:
                    stock = StockLevel(
                        product_id=product_id,
                        location_id=location_id,
                        qty_on_hand=quantity,
                        free_to_use=quantity
                    )
                    db.session.add(stock)
                else:
                    stock.qty_on_hand += quantity
                    stock.free_to_use += quantity
                
                # Create ledger entry
                ledger = StockLedger(
                    reference=operation.reference,
                    product_id=product_id,
                    to_location_id=location_id,
                    quantity=quantity,
                    operation_type='IN',
                    status='validated',
                    contact=operation.contact
                )
                db.session.add(ledger)
            
            elif operation.operation_type == 'OUT':
                # Decrease stock at from_location
                location_id = operation.from_location_id
                stock = StockLevel.query.filter_by(
                    product_id=product_id,
                    location_id=location_id
                ).first()
                
                if not stock:
                    return jsonify({'error': f'Insufficient stock for product {line.product.sku}'}), 400
                
                if float(stock.free_to_use) < quantity:
                    return jsonify({'error': f'Insufficient free stock for product {line.product.sku}'}), 400
                
                stock.qty_on_hand -= quantity
                stock.free_to_use -= quantity
                
                # Create ledger entry
                ledger = StockLedger(
                    reference=operation.reference,
                    product_id=product_id,
                    from_location_id=location_id,
                    quantity=quantity,
                    operation_type='OUT',
                    status='validated',
                    contact=operation.contact
                )
                db.session.add(ledger)
        
        operation.status = 'validated'
        operation.validated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(operation.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to validate operation: {str(e)}'}), 500

@operations_bp.route('/<int:operation_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_operation(operation_id):
    operation = Operation.query.get_or_404(operation_id)
    
    if operation.status != 'pending':
        return jsonify({'error': 'Only pending operations can be cancelled'}), 400
    
    operation.status = 'cancelled'
    
    try:
        db.session.commit()
        return jsonify(operation.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to cancel operation'}), 500

