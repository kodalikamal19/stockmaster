from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app import db
from app.models.operation import Operation, OperationLine, OperationType, OperationStatus
from app.models.warehouse import Warehouse
from app.models.location import Location
from app.models.product import Product
from app.utils.reference_generator import generate_reference
from app.services.stock_service import StockService
from datetime import datetime, date
from sqlalchemy import or_, and_

operations_bp = Blueprint('operations', __name__)
operations_ns = Namespace('operations', description='Operations management')

operation_line_model = operations_ns.model('OperationLine', {
    'product_id': fields.Integer(required=True),
    'quantity': fields.Integer(required=True),
    'unit_cost': fields.Float(),
    'notes': fields.String()
})

operation_model = operations_ns.model('Operation', {
    'operation_type': fields.String(required=True, enum=['IN', 'OUT', 'ADJ']),
    'warehouse_id': fields.Integer(required=True),
    'from_location_id': fields.Integer(),
    'to_location_id': fields.Integer(required=True),
    'contact_name': fields.String(),
    'contact_email': fields.String(),
    'contact_phone': fields.String(),
    'schedule_date': fields.String(),
    'notes': fields.String(),
    'lines': fields.List(fields.Nested(operation_line_model), required=True)
})


@operations_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics"""
    from app.services.operation_service import OperationService
    stats = OperationService.get_dashboard_stats()
    return jsonify(stats), 200


@operations_bp.route('/receipts', methods=['GET'])
@jwt_required()
def get_receipts():
    """Get all receipts with filters"""
    search = request.args.get('search', '')
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Operation.query.filter_by(operation_type=OperationType.RECEIPT)
    
    if search:
        query = query.filter(
            or_(
                Operation.reference.ilike(f'%{search}%'),
                Operation.contact_name.ilike(f'%{search}%')
            )
        )
    
    if status:
        try:
            status_enum = OperationStatus(status)
            query = query.filter_by(status=status_enum)
        except ValueError:
            pass
    
    receipts = query.order_by(Operation.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'items': [r.to_dict() for r in receipts.items],
        'total': receipts.total,
        'page': page,
        'per_page': per_page,
        'pages': receipts.pages
    }), 200


@operations_bp.route('/deliveries', methods=['GET'])
@jwt_required()
def get_deliveries():
    """Get all deliveries with filters"""
    search = request.args.get('search', '')
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Operation.query.filter_by(operation_type=OperationType.DELIVERY)
    
    if search:
        query = query.filter(
            or_(
                Operation.reference.ilike(f'%{search}%'),
                Operation.contact_name.ilike(f'%{search}%')
            )
        )
    
    if status:
        try:
            status_enum = OperationStatus(status)
            query = query.filter_by(status=status_enum)
        except ValueError:
            pass
    
    deliveries = query.order_by(Operation.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'items': [d.to_dict() for d in deliveries.items],
        'total': deliveries.total,
        'page': page,
        'per_page': per_page,
        'pages': deliveries.pages
    }), 200


@operations_bp.route('/adjustments', methods=['GET'])
@jwt_required()
def get_adjustments():
    """Get all adjustments"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    adjustments = Operation.query.filter_by(
        operation_type=OperationType.ADJUSTMENT
    ).order_by(Operation.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'items': [a.to_dict(include_lines=True) for a in adjustments.items],
        'total': adjustments.total,
        'page': page,
        'per_page': per_page,
        'pages': adjustments.pages
    }), 200


@operations_bp.route('/receipts', methods=['POST'])
@jwt_required()
def create_receipt():
    """Create a new receipt"""
    data = request.get_json()
    
    warehouse = Warehouse.query.get(data.get('warehouse_id'))
    if not warehouse:
        return jsonify({'error': 'Warehouse not found'}), 404
    
    to_location = Location.query.get(data.get('to_location_id'))
    if not to_location:
        return jsonify({'error': 'To location not found'}), 404
    
    # Generate reference
    reference = generate_reference(warehouse.short_code, OperationType.RECEIPT)
    
    # Parse schedule date
    schedule_date = None
    if data.get('schedule_date'):
        try:
            schedule_date = datetime.fromisoformat(data.get('schedule_date')).date()
        except:
            schedule_date = None
    
    # Determine status based on schedule date
    status = OperationStatus.PENDING
    if schedule_date:
        if schedule_date > date.today():
            status = OperationStatus.SCHEDULED
        elif schedule_date < date.today():
            status = OperationStatus.LATE
    
    # Create operation
    operation = Operation(
        reference=reference,
        operation_type=OperationType.RECEIPT,
        status=status,
        warehouse_id=data.get('warehouse_id'),
        to_location_id=data.get('to_location_id'),
        contact_name=data.get('contact_name'),
        contact_email=data.get('contact_email'),
        contact_phone=data.get('contact_phone'),
        schedule_date=schedule_date,
        notes=data.get('notes')
    )
    
    db.session.add(operation)
    db.session.flush()
    
    # Create operation lines
    for line_data in data.get('lines', []):
        product = Product.query.get(line_data.get('product_id'))
        if not product:
            db.session.rollback()
            return jsonify({'error': f'Product {line_data.get("product_id")} not found'}), 404
        
        line = OperationLine(
            operation_id=operation.id,
            product_id=line_data.get('product_id'),
            quantity=line_data.get('quantity'),
            unit_cost=line_data.get('unit_cost'),
            notes=line_data.get('notes')
        )
        db.session.add(line)
    
    db.session.commit()
    
    return jsonify(operation.to_dict(include_lines=True)), 201


@operations_bp.route('/deliveries', methods=['POST'])
@jwt_required()
def create_delivery():
    """Create a new delivery"""
    data = request.get_json()
    
    warehouse = Warehouse.query.get(data.get('warehouse_id'))
    if not warehouse:
        return jsonify({'error': 'Warehouse not found'}), 404
    
    to_location = Location.query.get(data.get('to_location_id'))
    if not to_location:
        return jsonify({'error': 'To location not found'}), 404
    
    # Generate reference
    reference = generate_reference(warehouse.short_code, OperationType.DELIVERY)
    
    # Parse schedule date
    schedule_date = None
    if data.get('schedule_date'):
        try:
            schedule_date = datetime.fromisoformat(data.get('schedule_date')).date()
        except:
            schedule_date = None
    
    # Determine status
    status = OperationStatus.PENDING
    if schedule_date:
        if schedule_date > date.today():
            status = OperationStatus.SCHEDULED
        elif schedule_date < date.today():
            status = OperationStatus.LATE
    
    # Create operation
    operation = Operation(
        reference=reference,
        operation_type=OperationType.DELIVERY,
        status=status,
        warehouse_id=data.get('warehouse_id'),
        from_location_id=data.get('from_location_id'),
        to_location_id=data.get('to_location_id'),
        contact_name=data.get('contact_name'),
        contact_email=data.get('contact_email'),
        contact_phone=data.get('contact_phone'),
        schedule_date=schedule_date,
        notes=data.get('notes')
    )
    
    db.session.add(operation)
    db.session.flush()
    
    # Create operation lines
    for line_data in data.get('lines', []):
        product = Product.query.get(line_data.get('product_id'))
        if not product:
            db.session.rollback()
            return jsonify({'error': f'Product {line_data.get("product_id")} not found'}), 404
        
        line = OperationLine(
            operation_id=operation.id,
            product_id=line_data.get('product_id'),
            quantity=line_data.get('quantity'),
            unit_cost=line_data.get('unit_cost'),
            notes=line_data.get('notes')
        )
        db.session.add(line)
    
    db.session.commit()
    
    return jsonify(operation.to_dict(include_lines=True)), 201


@operations_bp.route('/adjustments', methods=['POST'])
@jwt_required()
def create_adjustment():
    """Create a new adjustment"""
    data = request.get_json()
    
    warehouse = Warehouse.query.get(data.get('warehouse_id'))
    if not warehouse:
        return jsonify({'error': 'Warehouse not found'}), 404
    
    location = Location.query.get(data.get('to_location_id'))
    if not location:
        return jsonify({'error': 'Location not found'}), 404
    
    # Generate reference
    reference = generate_reference(warehouse.short_code, OperationType.ADJUSTMENT)
    
    # Create operation
    operation = Operation(
        reference=reference,
        operation_type=OperationType.ADJUSTMENT,
        status=OperationStatus.PENDING,
        warehouse_id=data.get('warehouse_id'),
        to_location_id=data.get('to_location_id'),
        notes=data.get('notes')
    )
    
    db.session.add(operation)
    db.session.flush()
    
    # Create operation line (adjustments typically have one line)
    line_data = data.get('lines', [{}])[0] if data.get('lines') else {}
    product = Product.query.get(line_data.get('product_id'))
    if not product:
        db.session.rollback()
        return jsonify({'error': 'Product not found'}), 404
    
    line = OperationLine(
        operation_id=operation.id,
        product_id=line_data.get('product_id'),
        quantity=line_data.get('quantity', 0),
        unit_cost=line_data.get('unit_cost'),
        notes=line_data.get('notes')
    )
    db.session.add(line)
    
    db.session.commit()
    
    return jsonify(operation.to_dict(include_lines=True)), 201


@operations_bp.route('/<int:operation_id>', methods=['GET'])
@jwt_required()
def get_operation(operation_id):
    """Get operation details"""
    operation = Operation.query.get_or_404(operation_id)
    return jsonify(operation.to_dict(include_lines=True)), 200


@operations_bp.route('/<int:operation_id>/validate', methods=['POST'])
@jwt_required()
def validate_operation(operation_id):
    """Validate an operation (updates stock)"""
    operation = Operation.query.get_or_404(operation_id)
    current_user_id = get_jwt_identity()
    
    if operation.status == OperationStatus.VALIDATED:
        return jsonify({'error': 'Operation already validated'}), 400
    
    if operation.status == OperationStatus.CANCELLED:
        return jsonify({'error': 'Cannot validate cancelled operation'}), 400
    
    # Update stock
    StockService.update_stock_on_operation(operation)
    
    # Update operation status
    operation.status = OperationStatus.VALIDATED
    operation.validated_at = datetime.utcnow()
    operation.validated_by = current_user_id
    
    db.session.commit()
    
    return jsonify(operation.to_dict(include_lines=True)), 200


@operations_bp.route('/<int:operation_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_operation(operation_id):
    """Cancel an operation"""
    operation = Operation.query.get_or_404(operation_id)
    current_user_id = get_jwt_identity()
    
    if operation.status == OperationStatus.VALIDATED:
        return jsonify({'error': 'Cannot cancel validated operation'}), 400
    
    if operation.status == OperationStatus.CANCELLED:
        return jsonify({'error': 'Operation already cancelled'}), 400
    
    operation.status = OperationStatus.CANCELLED
    operation.cancelled_at = datetime.utcnow()
    operation.cancelled_by = current_user_id
    
    db.session.commit()
    
    return jsonify(operation.to_dict(include_lines=True)), 200


# RESTX Resources
@operations_ns.route('/dashboard/stats')
class DashboardStats(Resource):
    @jwt_required()
    @operations_ns.doc('get_dashboard_stats')
    def get(self):
        return get_dashboard_stats()


@operations_ns.route('/receipts')
class Receipts(Resource):
    @jwt_required()
    @operations_ns.doc('get_receipts')
    def get(self):
        return get_receipts()
    
    @jwt_required()
    @operations_ns.expect(operation_model)
    @operations_ns.doc('create_receipt')
    def post(self):
        return create_receipt()


@operations_ns.route('/deliveries')
class Deliveries(Resource):
    @jwt_required()
    @operations_ns.doc('get_deliveries')
    def get(self):
        return get_deliveries()
    
    @jwt_required()
    @operations_ns.expect(operation_model)
    @operations_ns.doc('create_delivery')
    def post(self):
        return create_delivery()


@operations_ns.route('/adjustments')
class Adjustments(Resource):
    @jwt_required()
    @operations_ns.doc('get_adjustments')
    def get(self):
        return get_adjustments()
    
    @jwt_required()
    @operations_ns.expect(operation_model)
    @operations_ns.doc('create_adjustment')
    def post(self):
        return create_adjustment()


@operations_ns.route('/<int:operation_id>')
class OperationDetail(Resource):
    @jwt_required()
    @operations_ns.doc('get_operation')
    def get(self, operation_id):
        return get_operation(operation_id)


@operations_ns.route('/<int:operation_id>/validate')
class ValidateOperation(Resource):
    @jwt_required()
    @operations_ns.doc('validate_operation')
    def post(self, operation_id):
        return validate_operation(operation_id)


@operations_ns.route('/<int:operation_id>/cancel')
class CancelOperation(Resource):
    @jwt_required()
    @operations_ns.doc('cancel_operation')
    def post(self, operation_id):
        return cancel_operation(operation_id)

