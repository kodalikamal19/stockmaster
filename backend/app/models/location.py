from app import db
from datetime import datetime


class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    short_code = db.Column(db.String(10), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stock_levels = db.relationship('StockLevel', backref='location', lazy='dynamic')
    
    # Unique constraint on short_code per warehouse
    __table_args__ = (db.UniqueConstraint('warehouse_id', 'short_code', name='uq_location_warehouse_short_code'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_code': self.short_code,
            'warehouse_id': self.warehouse_id,
            'warehouse_short_code': self.warehouse.short_code if self.warehouse else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

