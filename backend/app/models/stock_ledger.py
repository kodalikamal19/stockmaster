from app import db
from datetime import datetime
import enum


class LedgerType(enum.Enum):
    INBOUND = 'inbound'
    OUTBOUND = 'outbound'
    ADJUSTMENT = 'adjustment'
    TRANSFER = 'transfer'


class StockLedger(db.Model):
    __tablename__ = 'stock_ledger'
    
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50), nullable=False, index=True)
    ledger_type = db.Column(db.Enum(LedgerType), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Numeric(10, 2))
    operation_id = db.Column(db.Integer, db.ForeignKey('operations.id'))
    from_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    to_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    contact_name = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    product = db.relationship('Product', backref='ledger_entries')
    location = db.relationship('Location', foreign_keys=[location_id], backref='ledger_entries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'reference': self.reference,
            'ledger_type': self.ledger_type.value if self.ledger_type else None,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'location_id': self.location_id,
            'location': self.location.to_dict() if self.location else None,
            'quantity': self.quantity,
            'unit_cost': float(self.unit_cost) if self.unit_cost else None,
            'operation_id': self.operation_id,
            'from_location_id': self.from_location_id,
            'from_location': None,  # Can be populated if needed
            'to_location_id': self.to_location_id,
            'to_location': None,  # Can be populated if needed
            'contact_name': self.contact_name,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

