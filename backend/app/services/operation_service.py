from app import db
from app.models.operation import Operation, OperationStatus
from datetime import date
from sqlalchemy import and_, or_


class OperationService:
    @staticmethod
    def get_operation_stats(operation_type):
        """Get statistics for operations (receipts/deliveries)"""
        today = date.today()
        
        pending = Operation.query.filter_by(
            operation_type=operation_type,
            status=OperationStatus.PENDING
        ).count()
        
        scheduled = Operation.query.filter(
            and_(
                Operation.operation_type == operation_type,
                Operation.status == OperationStatus.SCHEDULED,
                Operation.schedule_date > today
            )
        ).count()
        
        late = Operation.query.filter(
            and_(
                Operation.operation_type == operation_type,
                Operation.status.in_([OperationStatus.PENDING, OperationStatus.SCHEDULED]),
                Operation.schedule_date < today
            )
        ).count()
        
        waiting_for_stock = Operation.query.filter_by(
            operation_type=operation_type,
            status=OperationStatus.WAITING_FOR_STOCK
        ).count()
        
        return {
            'pending': pending,
            'scheduled': scheduled,
            'late': late,
            'waiting_for_stock': waiting_for_stock,
            'total': pending + scheduled + late + waiting_for_stock
        }
    
    @staticmethod
    def get_dashboard_stats():
        """Get all dashboard statistics"""
        from app.models.operation import OperationType
        from app.models.product import Product
        from app.models.stock_level import StockLevel
        
        receipt_stats = OperationService.get_operation_stats(OperationType.RECEIPT)
        delivery_stats = OperationService.get_operation_stats(OperationType.DELIVERY)
        
        # Total stock items
        total_stock_items = StockLevel.query.count()
        
        # Low stock (quantity_on_hand < 10)
        low_stock = StockLevel.query.filter(
            StockLevel.quantity_on_hand < 10
        ).count()
        
        # Total operations left (pending + scheduled)
        total_operations = Operation.query.filter(
            Operation.status.in_([OperationStatus.PENDING, OperationStatus.SCHEDULED])
        ).count()
        
        return {
            'receipts': receipt_stats,
            'deliveries': delivery_stats,
            'total_stock_items': total_stock_items,
            'low_stock': low_stock,
            'operations_left': total_operations
        }

