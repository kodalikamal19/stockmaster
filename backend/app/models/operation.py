from app import db
from datetime import datetime
import enum


class OperationType(enum.Enum):
    RECEIPT = 'IN'
    DELIVERY = 'OUT'
    ADJUSTMENT = 'ADJ'


class OperationStatus(enum.Enum):
    PENDING = 'pending'
    SCHEDULED = 'scheduled'
    VALIDATED = 'validated'
    CANCELLED = 'cancelled'
    WAITING_FOR_STOCK = 'waiting_for_stock'
    LATE = 'late'


class Operation(db.Model):
    __tablename__ = 'operations'
    
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50), unique=True, nullable=False, index=True)
    operation_type = db.Column(db.Enum(OperationType), nullable=False, index=True)
    status = db.Column(db.Enum(OperationStatus), default=OperationStatus.PENDING, nullable=False, index=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    from_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    to_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    contact_name = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(50))
    schedule_date = db.Column(db.Date, index=True)
    validated_at = db.Column(db.DateTime)
    validated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    cancelled_at = db.Column(db.DateTime)
    cancelled_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lines = db.relationship('OperationLine', backref='operation', lazy='dynamic', cascade='all, delete-orphan')
    from_location = db.relationship('Location', foreign_keys=[from_location_id], backref='operations_from')
    to_location = db.relationship('Location', foreign_keys=[to_location_id], backref='operations_to')
    
    def to_dict(self, include_lines=False):
        data = {
            'id': self.id,
            'reference': self.reference,
            'operation_type': self.operation_type.value if self.operation_type else None,
            'status': self.status.value if self.status else None,
            'warehouse_id': self.warehouse_id,
            'warehouse_short_code': self.warehouse.short_code if self.warehouse else None,
            'from_location_id': self.from_location_id,
            'from_location': self.from_location.to_dict() if self.from_location else None,
            'to_location_id': self.to_location_id,
            'to_location': self.to_location.to_dict() if self.to_location else None,
            'contact_name': self.contact_name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'schedule_date': self.schedule_date.isoformat() if self.schedule_date else None,
            'validated_at': self.validated_at.isoformat() if self.validated_at else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_lines:
            data['lines'] = [line.to_dict() for line in self.lines]
        
        return data


class OperationLine(db.Model):
    __tablename__ = 'operation_lines'
    
    id = db.Column(db.Integer, primary_key=True)
    operation_id = db.Column(db.Integer, db.ForeignKey('operations.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Numeric(10, 2))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'operation_id': self.operation_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'unit_cost': float(self.unit_cost) if self.unit_cost else None,
            'notes': self.notes,
        }

