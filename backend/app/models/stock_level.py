from app import db
from datetime import datetime


class StockLevel(db.Model):
    __tablename__ = 'stock_levels'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    quantity_on_hand = db.Column(db.Integer, default=0, nullable=False)
    quantity_free_to_use = db.Column(db.Integer, default=0, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint on product + location
    __table_args__ = (db.UniqueConstraint('product_id', 'location_id', name='uq_stock_product_location'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'location_id': self.location_id,
            'location': self.location.to_dict() if self.location else None,
            'quantity_on_hand': self.quantity_on_hand,
            'quantity_free_to_use': self.quantity_free_to_use,
            'unit_cost': float(self.product.unit_cost) if self.product else 0.0,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

