from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(12), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'login_id': self.login_id,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class OTP(db.Model):
    __tablename__ = 'otps'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    otp_code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    locations = db.relationship('Location', backref='warehouse', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_code': self.short_code,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Location(db.Model):
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_code = db.Column(db.String(20), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('short_code', 'warehouse_id', name='unique_location_per_warehouse'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_code': self.short_code,
            'warehouse_id': self.warehouse_id,
            'warehouse_short_code': self.warehouse.short_code if self.warehouse else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    unit_cost = db.Column(db.Numeric(10, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sku': self.sku,
            'unit_cost': float(self.unit_cost) if self.unit_cost else 0.0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class StockLevel(db.Model):
    __tablename__ = 'stock_levels'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    qty_on_hand = db.Column(db.Numeric(10, 2), default=0.00)
    free_to_use = db.Column(db.Numeric(10, 2), default=0.00)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    product = db.relationship('Product', backref='stock_levels')
    location = db.relationship('Location', backref='stock_levels')
    
    __table_args__ = (db.UniqueConstraint('product_id', 'location_id', name='unique_stock_per_location'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'product_sku': self.product.sku if self.product else None,
            'location_id': self.location_id,
            'location_name': self.location.name if self.location else None,
            'location_short_code': self.location.short_code if self.location else None,
            'warehouse_short_code': self.location.warehouse.short_code if self.location and self.location.warehouse else None,
            'qty_on_hand': float(self.qty_on_hand) if self.qty_on_hand else 0.0,
            'free_to_use': float(self.free_to_use) if self.free_to_use else 0.0,
            'unit_cost': float(self.product.unit_cost) if self.product else 0.0,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Operation(db.Model):
    __tablename__ = 'operations'
    
    OPERATION_TYPES = {
        'IN': 'Receipt',
        'OUT': 'Delivery',
        'ADJ': 'Adjustment'
    }
    
    STATUS_CHOICES = ['pending', 'validated', 'cancelled']
    
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50), unique=True, nullable=False, index=True)
    operation_type = db.Column(db.String(10), nullable=False)  # IN, OUT, ADJ
    from_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    to_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    contact = db.Column(db.String(200))
    schedule_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    validated_at = db.Column(db.DateTime, nullable=True)
    
    from_location = db.relationship('Location', foreign_keys=[from_location_id], backref='outbound_operations')
    to_location = db.relationship('Location', foreign_keys=[to_location_id], backref='inbound_operations')
    lines = db.relationship('OperationLine', backref='operation', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'reference': self.reference,
            'operation_type': self.operation_type,
            'operation_type_name': self.OPERATION_TYPES.get(self.operation_type, self.operation_type),
            'from_location_id': self.from_location_id,
            'from_location_name': self.from_location.name if self.from_location else None,
            'from_warehouse': self.from_location.warehouse.short_code if self.from_location and self.from_location.warehouse else None,
            'to_location_id': self.to_location_id,
            'to_location_name': self.to_location.name if self.to_location else None,
            'to_warehouse': self.to_location.warehouse.short_code if self.to_location and self.to_location.warehouse else None,
            'contact': self.contact,
            'schedule_date': self.schedule_date.isoformat() if self.schedule_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'validated_at': self.validated_at.isoformat() if self.validated_at else None,
            'lines': [line.to_dict() for line in self.lines]
        }

class OperationLine(db.Model):
    __tablename__ = 'operation_lines'
    
    id = db.Column(db.Integer, primary_key=True)
    operation_id = db.Column(db.Integer, db.ForeignKey('operations.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    unit_cost = db.Column(db.Numeric(10, 2), nullable=False)
    
    product = db.relationship('Product', backref='operation_lines')
    
    def to_dict(self):
        return {
            'id': self.id,
            'operation_id': self.operation_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'product_sku': self.product.sku if self.product else None,
            'quantity': float(self.quantity) if self.quantity else 0.0,
            'unit_cost': float(self.unit_cost) if self.unit_cost else 0.0
        }

class StockLedger(db.Model):
    __tablename__ = 'stock_ledger'
    
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50), nullable=False, index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    from_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    to_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    operation_type = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    contact = db.Column(db.String(200))
    
    product = db.relationship('Product', backref='ledger_entries')
    from_location = db.relationship('Location', foreign_keys=[from_location_id], backref='outbound_ledger')
    to_location = db.relationship('Location', foreign_keys=[to_location_id], backref='inbound_ledger')
    
    def to_dict(self):
        return {
            'id': self.id,
            'reference': self.reference,
            'date': self.date.isoformat() if self.date else None,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'product_sku': self.product.sku if self.product else None,
            'from_location_id': self.from_location_id,
            'from_location_name': self.from_location.name if self.from_location else None,
            'from_warehouse': self.from_location.warehouse.short_code if self.from_location and self.from_location.warehouse else None,
            'to_location_id': self.to_location_id,
            'to_location_name': self.to_location.name if self.to_location else None,
            'to_warehouse': self.to_location.warehouse.short_code if self.to_location and self.to_location.warehouse else None,
            'quantity': float(self.quantity) if self.quantity else 0.0,
            'operation_type': self.operation_type,
            'status': self.status,
            'contact': self.contact
        }

