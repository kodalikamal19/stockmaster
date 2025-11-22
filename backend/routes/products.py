from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Product

products_bp = Blueprint('products', __name__)

@products_bp.route('', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200

@products_bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    
    name = data.get('name', '').strip()
    sku = data.get('sku', '').strip().upper()
    unit_cost = data.get('unit_cost', 0.0)
    
    if not name or not sku:
        return jsonify({'error': 'Name and SKU are required'}), 400
    
    if Product.query.filter_by(sku=sku).first():
        return jsonify({'error': 'SKU already exists'}), 400
    
    product = Product(name=name, sku=sku, unit_cost=unit_cost)
    
    try:
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create product'}), 500

@products_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict()), 200

@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    name = data.get('name', '').strip()
    sku = data.get('sku', '').strip().upper()
    unit_cost = data.get('unit_cost', 0.0)
    
    if not name or not sku:
        return jsonify({'error': 'Name and SKU are required'}), 400
    
    if sku != product.sku:
        if Product.query.filter_by(sku=sku).first():
            return jsonify({'error': 'SKU already exists'}), 400
    
    product.name = name
    product.sku = sku
    product.unit_cost = unit_cost
    
    try:
        db.session.commit()
        return jsonify(product.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update product'}), 500

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete product'}), 500

