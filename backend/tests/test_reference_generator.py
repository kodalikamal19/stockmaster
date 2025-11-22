import pytest
from app import create_app, db
from app.models.operation import Operation, OperationType
from app.models.warehouse import Warehouse
from app.utils.reference_generator import generate_reference
import threading


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        # Create test warehouse
        warehouse = Warehouse(name='Test Warehouse', short_code='WH1')
        db.session.add(warehouse)
        db.session.commit()
        yield app
        db.drop_all()


def test_generate_reference_first(app):
    """Test generating first reference"""
    with app.app_context():
        ref = generate_reference('WH1', OperationType.RECEIPT)
        assert ref == 'WH1/IN/0001'


def test_generate_reference_increment(app):
    """Test reference increments correctly"""
    with app.app_context():
        # Create existing operation
        from app.models.operation import OperationStatus
        operation = Operation(
            reference='WH1/IN/0001',
            operation_type=OperationType.RECEIPT,
            status=OperationStatus.PENDING,
            warehouse_id=1,
            to_location_id=1
        )
        db.session.add(operation)
        db.session.commit()
        
        ref = generate_reference('WH1', OperationType.RECEIPT)
        assert ref == 'WH1/IN/0002'


def test_generate_reference_different_types(app):
    """Test different operation types get different sequences"""
    with app.app_context():
        ref1 = generate_reference('WH1', OperationType.RECEIPT)
        ref2 = generate_reference('WH1', OperationType.DELIVERY)
        ref3 = generate_reference('WH1', OperationType.ADJUSTMENT)
        
        assert ref1 == 'WH1/IN/0001'
        assert ref2 == 'WH1/OUT/0001'
        assert ref3 == 'WH1/ADJ/0001'

