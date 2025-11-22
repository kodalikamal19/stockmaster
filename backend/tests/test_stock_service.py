import pytest
from app import create_app, db
from app.models.operation import Operation, OperationType, OperationStatus
from app.models.product import Product
from app.models.location import Location
from app.models.warehouse import Warehouse
from app.models.stock_level import StockLevel
from app.models.operation_line import OperationLine
from app.services.stock_service import StockService


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        # Create test data
        warehouse = Warehouse(name='Test Warehouse', short_code='WH1')
        db.session.add(warehouse)
        location = Location(name='Location 1', short_code='LOC1', warehouse_id=1)
        db.session.add(location)
        product = Product(name='Test Product', sku='TEST-001', unit_cost=10.00)
        db.session.add(product)
        db.session.commit()
        yield app
        db.drop_all()


def test_update_stock_on_receipt(app):
    """Test stock increases on receipt validation"""
    with app.app_context():
        operation = Operation(
            reference='WH1/IN/0001',
            operation_type=OperationType.RECEIPT,
            status=OperationStatus.PENDING,
            warehouse_id=1,
            to_location_id=1
        )
        db.session.add(operation)
        db.session.flush()
        
        line = OperationLine(
            operation_id=operation.id,
            product_id=1,
            quantity=10
        )
        db.session.add(line)
        db.session.commit()
        
        operation.status = OperationStatus.VALIDATED
        StockService.update_stock_on_operation(operation)
        
        stock = StockLevel.query.filter_by(product_id=1, location_id=1).first()
        assert stock is not None
        assert stock.quantity_on_hand == 10
        assert stock.quantity_free_to_use == 10


def test_update_stock_on_delivery(app):
    """Test stock decreases on delivery validation"""
    with app.app_context():
        # First create stock
        stock = StockLevel(product_id=1, location_id=1, quantity_on_hand=20, quantity_free_to_use=20)
        db.session.add(stock)
        db.session.commit()
        
        operation = Operation(
            reference='WH1/OUT/0001',
            operation_type=OperationType.DELIVERY,
            status=OperationStatus.PENDING,
            warehouse_id=1,
            to_location_id=1
        )
        db.session.add(operation)
        db.session.flush()
        
        line = OperationLine(
            operation_id=operation.id,
            product_id=1,
            quantity=5
        )
        db.session.add(line)
        db.session.commit()
        
        operation.status = OperationStatus.VALIDATED
        StockService.update_stock_on_operation(operation)
        
        stock = StockLevel.query.filter_by(product_id=1, location_id=1).first()
        assert stock.quantity_on_hand == 15
        assert stock.quantity_free_to_use == 15

