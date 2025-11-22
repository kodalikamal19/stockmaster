from app import create_app, db
from app.models.user import User
from app.models.warehouse import Warehouse
from app.models.location import Location
from app.models.product import Product
from faker import Faker

fake = Faker()


def seed_data():
    app = create_app()
    with app.app_context():
        # Clear existing data (optional - comment out in production)
        # db.drop_all()
        # db.create_all()
        
        # Create admin user
        admin = User.query.filter_by(login_id='admin').first()
        if not admin:
            admin = User(
                login_id='admin',
                email='admin@stockmaster.com',
                first_name='Admin',
                last_name='User'
            )
            admin.set_password('Admin123!')
            db.session.add(admin)
            print("Created admin user: admin / Admin123!")
        
        # Create test user
        test_user = User.query.filter_by(login_id='testuser').first()
        if not test_user:
            test_user = User(
                login_id='testuser',
                email='test@stockmaster.com',
                first_name='Test',
                last_name='User'
            )
            test_user.set_password('Test123!')
            db.session.add(test_user)
            print("Created test user: testuser / Test123!")
        
        # Create warehouses
        warehouses_data = [
            {'name': 'Main Warehouse', 'short_code': 'WH1', 'address': '123 Main St, City, State 12345'},
            {'name': 'Secondary Warehouse', 'short_code': 'WH2', 'address': '456 Oak Ave, City, State 12345'},
            {'name': 'Distribution Center', 'short_code': 'DC1', 'address': '789 Pine Rd, City, State 12345'},
        ]
        
        for wh_data in warehouses_data:
            warehouse = Warehouse.query.filter_by(short_code=wh_data['short_code']).first()
            if not warehouse:
                warehouse = Warehouse(**wh_data)
                db.session.add(warehouse)
                print(f"Created warehouse: {warehouse.short_code}")
        
        db.session.flush()
        
        # Create locations for each warehouse
        warehouses = Warehouse.query.all()
        location_names = ['Aisle 1', 'Aisle 2', 'Aisle 3', 'Cold Storage', 'Loading Dock']
        
        for warehouse in warehouses:
            for i, loc_name in enumerate(location_names):
                location = Location.query.filter_by(
                    warehouse_id=warehouse.id,
                    short_code=f'LOC{i+1}'
                ).first()
                if not location:
                    location = Location(
                        name=f"{warehouse.short_code} - {loc_name}",
                        short_code=f'LOC{i+1}',
                        warehouse_id=warehouse.id
                    )
                    db.session.add(location)
                    print(f"Created location: {location.short_code} in {warehouse.short_code}")
        
        db.session.flush()
        
        # Create products
        products_data = [
            {'name': 'Widget A', 'sku': 'WID-A-001', 'unit_cost': 10.50, 'description': 'Standard widget'},
            {'name': 'Widget B', 'sku': 'WID-B-002', 'unit_cost': 15.75, 'description': 'Premium widget'},
            {'name': 'Gadget X', 'sku': 'GAD-X-100', 'unit_cost': 25.00, 'description': 'Electronic gadget'},
            {'name': 'Gadget Y', 'sku': 'GAD-Y-200', 'unit_cost': 30.50, 'description': 'Advanced gadget'},
            {'name': 'Tool Set 1', 'sku': 'TOOL-001', 'unit_cost': 45.00, 'description': 'Basic tool set'},
            {'name': 'Tool Set 2', 'sku': 'TOOL-002', 'unit_cost': 65.00, 'description': 'Professional tool set'},
            {'name': 'Component A', 'sku': 'COMP-A-01', 'unit_cost': 5.25, 'description': 'Small component'},
            {'name': 'Component B', 'sku': 'COMP-B-02', 'unit_cost': 8.75, 'description': 'Medium component'},
            {'name': 'Material X', 'sku': 'MAT-X-100', 'unit_cost': 12.00, 'description': 'Raw material'},
            {'name': 'Material Y', 'sku': 'MAT-Y-200', 'unit_cost': 18.50, 'description': 'Processed material'},
        ]
        
        for prod_data in products_data:
            product = Product.query.filter_by(sku=prod_data['sku']).first()
            if not product:
                product = Product(**prod_data)
                db.session.add(product)
                print(f"Created product: {product.sku}")
        
        db.session.commit()
        print("\nSeed data created successfully!")


if __name__ == '__main__':
    seed_data()

