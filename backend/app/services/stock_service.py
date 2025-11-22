from app import db
from app.models.stock_level import StockLevel
from app.models.stock_ledger import StockLedger, LedgerType
from app.models.operation import Operation, OperationType, OperationStatus
from datetime import datetime


class StockService:
    @staticmethod
    def update_stock_on_operation(operation):
        """Update stock levels when an operation is validated"""
        if operation.status != OperationStatus.VALIDATED:
            return
        
        for line in operation.lines:
            # Get or create stock level
            stock_level = StockLevel.query.filter_by(
                product_id=line.product_id,
                location_id=operation.to_location_id
            ).first()
            
            if not stock_level:
                stock_level = StockLevel(
                    product_id=line.product_id,
                    location_id=operation.to_location_id,
                    quantity_on_hand=0,
                    quantity_free_to_use=0
                )
                db.session.add(stock_level)
            
            if operation.operation_type == OperationType.RECEIPT:
                # Increase stock
                stock_level.quantity_on_hand += line.quantity
                stock_level.quantity_free_to_use += line.quantity
                
                # Create ledger entry
                ledger_entry = StockLedger(
                    reference=operation.reference,
                    ledger_type=LedgerType.INBOUND,
                    product_id=line.product_id,
                    location_id=operation.to_location_id,
                    quantity=line.quantity,
                    unit_cost=line.unit_cost or stock_level.product.unit_cost,
                    operation_id=operation.id,
                    contact_name=operation.contact_name,
                    notes=f"Receipt: {operation.reference}"
                )
                db.session.add(ledger_entry)
                
            elif operation.operation_type == OperationType.DELIVERY:
                # Decrease stock
                if stock_level.quantity_on_hand >= line.quantity:
                    stock_level.quantity_on_hand -= line.quantity
                    stock_level.quantity_free_to_use -= line.quantity
                else:
                    # Handle insufficient stock
                    stock_level.quantity_on_hand = 0
                    stock_level.quantity_free_to_use = 0
                
                # Create ledger entry
                ledger_entry = StockLedger(
                    reference=operation.reference,
                    ledger_type=LedgerType.OUTBOUND,
                    product_id=line.product_id,
                    location_id=operation.to_location_id,
                    quantity=-line.quantity,
                    unit_cost=line.unit_cost or stock_level.product.unit_cost,
                    operation_id=operation.id,
                    contact_name=operation.contact_name,
                    notes=f"Delivery: {operation.reference}"
                )
                db.session.add(ledger_entry)
            
            elif operation.operation_type == OperationType.ADJUSTMENT:
                # Adjust stock to counted quantity
                stock_level.quantity_on_hand = line.quantity
                stock_level.quantity_free_to_use = line.quantity
                
                # Create ledger entry
                ledger_entry = StockLedger(
                    reference=operation.reference,
                    ledger_type=LedgerType.ADJUSTMENT,
                    product_id=line.product_id,
                    location_id=operation.to_location_id,
                    quantity=line.quantity,
                    unit_cost=line.unit_cost or stock_level.product.unit_cost,
                    operation_id=operation.id,
                    notes=f"Adjustment: {operation.reference}"
                )
                db.session.add(ledger_entry)
        
        db.session.commit()
    
    @staticmethod
    def get_stock_level(product_id, location_id):
        """Get stock level for a product at a location"""
        stock_level = StockLevel.query.filter_by(
            product_id=product_id,
            location_id=location_id
        ).first()
        
        if not stock_level:
            return {
                'quantity_on_hand': 0,
                'quantity_free_to_use': 0
            }
        
        return {
            'quantity_on_hand': stock_level.quantity_on_hand,
            'quantity_free_to_use': stock_level.quantity_free_to_use
        }

