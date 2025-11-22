from app import db
from app.models.operation import Operation, OperationType
from sqlalchemy import func
import threading

# Thread lock for safe concurrency
_reference_lock = threading.Lock()


def generate_reference(warehouse_short_code, operation_type):
    """
    Generate a unique reference in format: <WarehouseShortCode>/<OperationType>/<AutoIncrementID>
    Example: WH1/IN/0001
    
    Thread-safe implementation to prevent conflicts.
    """
    with _reference_lock:
        # Map operation type to code
        type_map = {
            OperationType.RECEIPT: 'IN',
            OperationType.DELIVERY: 'OUT',
            OperationType.ADJUSTMENT: 'ADJ'
        }
        
        type_code = type_map.get(operation_type, 'OP')
        prefix = f"{warehouse_short_code}/{type_code}/"
        
        # Find the highest existing number for this prefix
        last_ref = db.session.query(Operation.reference).filter(
            Operation.reference.like(f"{prefix}%")
        ).order_by(Operation.reference.desc()).first()
        
        if last_ref:
            # Extract the number part
            last_num = int(last_ref[0].split('/')[-1])
            next_num = last_num + 1
        else:
            next_num = 1
        
        # Format with zero padding (4 digits)
        reference = f"{prefix}{next_num:04d}"
        
        # Double-check uniqueness (safety check)
        exists = db.session.query(Operation).filter_by(reference=reference).first()
        if exists:
            # If somehow exists, increment and try again
            next_num += 1
            reference = f"{prefix}{next_num:04d}"
        
        return reference

