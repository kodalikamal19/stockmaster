-- Sample Data for StockMaster
-- Run this script in pgAdmin Query Tool or psql

-- 1. Insert Sample Users
-- IMPORTANT: To generate a proper password hash, run: python generate_password_hash.py
-- Then replace the hash below with the generated hash
-- OR simply create users via the signup page in the application

-- For now, you can create users via the signup page, or uncomment and update the hash below:
-- INSERT INTO users (login_id, email, password_hash, created_at) VALUES
-- ('admin001', 'admin@stockmaster.com', 'GENERATED_HASH_HERE', NOW()),
-- ('user001', 'user@stockmaster.com', 'GENERATED_HASH_HERE', NOW())
-- ON CONFLICT (login_id) DO NOTHING;

-- RECOMMENDED: Create users via the signup page at http://localhost:3000/signup

-- 2. Insert Sample Warehouses
INSERT INTO warehouses (name, short_code, address, created_at) VALUES
('Main Warehouse', 'WH1', '123 Industrial Street, City, State 12345', NOW()),
('Secondary Warehouse', 'WH2', '456 Commerce Avenue, City, State 12345', NOW()),
('Distribution Center', 'WH3', '789 Logistics Road, City, State 12345', NOW())
ON CONFLICT (short_code) DO NOTHING;

-- 3. Insert Sample Locations
INSERT INTO locations (name, short_code, warehouse_id, created_at) VALUES
('Aisle 1', 'A1', (SELECT id FROM warehouses WHERE short_code = 'WH1'), NOW()),
('Aisle 2', 'A2', (SELECT id FROM warehouses WHERE short_code = 'WH1'), NOW()),
('Cold Storage', 'CS1', (SELECT id FROM warehouses WHERE short_code = 'WH1'), NOW()),
('Loading Dock', 'LD1', (SELECT id FROM warehouses WHERE short_code = 'WH1'), NOW()),
('Section A', 'SA1', (SELECT id FROM warehouses WHERE short_code = 'WH2'), NOW()),
('Section B', 'SB1', (SELECT id FROM warehouses WHERE short_code = 'WH2'), NOW()),
('Zone 1', 'Z1', (SELECT id FROM warehouses WHERE short_code = 'WH3'), NOW()),
('Zone 2', 'Z2', (SELECT id FROM warehouses WHERE short_code = 'WH3'), NOW())
ON CONFLICT (short_code, warehouse_id) DO NOTHING;

-- 4. Insert Sample Products (Prices in Indian Rupees - ₹)
-- Conversion rate: 1 USD = 83.5 INR (approximate)
INSERT INTO products (name, sku, unit_cost, created_at) VALUES
('Laptop Computer', 'LAP-001', 75149.17, NOW()),
('Wireless Mouse', 'MSE-001', 2504.17, NOW()),
('Keyboard Mechanical', 'KBD-001', 6679.17, NOW()),
('Monitor 27 inch', 'MON-001', 25049.17, NOW()),
('USB Cable Type-C', 'CBL-001', 1084.67, NOW()),
('Webcam HD', 'CAM-001', 4174.17, NOW()),
('Headphones Wireless', 'HP-001', 10854.17, NOW()),
('External Hard Drive 1TB', 'HDD-001', 5009.17, NOW()),
('SSD 500GB', 'SSD-001', 7509.17, NOW()),
('RAM 16GB DDR4', 'RAM-001', 6679.17, NOW()),
('Graphics Card RTX 3060', 'GPU-001', 33399.17, NOW()),
('Power Supply 650W', 'PSU-001', 7509.17, NOW()),
('Motherboard ATX', 'MB-001', 16699.17, NOW()),
('CPU Cooler', 'CPU-C-001', 4174.17, NOW()),
('Case Mid Tower', 'CASE-001', 6679.17, NOW())
ON CONFLICT (sku) DO NOTHING;

-- 5. Insert Sample Stock Levels
INSERT INTO stock_levels (product_id, location_id, qty_on_hand, free_to_use, updated_at) VALUES
-- Warehouse 1, Location A1
((SELECT id FROM products WHERE sku = 'LAP-001'), (SELECT id FROM locations WHERE short_code = 'A1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 50, 45, NOW()),
((SELECT id FROM products WHERE sku = 'MSE-001'), (SELECT id FROM locations WHERE short_code = 'A1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 200, 180, NOW()),
((SELECT id FROM products WHERE sku = 'KBD-001'), (SELECT id FROM locations WHERE short_code = 'A1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 100, 95, NOW()),
-- Warehouse 1, Location A2
((SELECT id FROM products WHERE sku = 'MON-001'), (SELECT id FROM locations WHERE short_code = 'A2' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 75, 70, NOW()),
((SELECT id FROM products WHERE sku = 'CBL-001'), (SELECT id FROM locations WHERE short_code = 'A2' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 500, 480, NOW()),
((SELECT id FROM products WHERE sku = 'CAM-001'), (SELECT id FROM locations WHERE short_code = 'A2' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 150, 140, NOW()),
-- Warehouse 1, Location CS1
((SELECT id FROM products WHERE sku = 'HP-001'), (SELECT id FROM locations WHERE short_code = 'CS1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 80, 75, NOW()),
((SELECT id FROM products WHERE sku = 'HDD-001'), (SELECT id FROM locations WHERE short_code = 'CS1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 120, 110, NOW()),
-- Warehouse 2
((SELECT id FROM products WHERE sku = 'SSD-001'), (SELECT id FROM locations WHERE short_code = 'SA1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH2')), 200, 190, NOW()),
((SELECT id FROM products WHERE sku = 'RAM-001'), (SELECT id FROM locations WHERE short_code = 'SA1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH2')), 300, 280, NOW()),
((SELECT id FROM products WHERE sku = 'GPU-001'), (SELECT id FROM locations WHERE short_code = 'SB1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH2')), 40, 35, NOW()),
((SELECT id FROM products WHERE sku = 'PSU-001'), (SELECT id FROM locations WHERE short_code = 'SB1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH2')), 100, 95, NOW()),
-- Warehouse 3
((SELECT id FROM products WHERE sku = 'MB-001'), (SELECT id FROM locations WHERE short_code = 'Z1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH3')), 60, 55, NOW()),
((SELECT id FROM products WHERE sku = 'CPU-C-001'), (SELECT id FROM locations WHERE short_code = 'Z1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH3')), 150, 140, NOW()),
((SELECT id FROM products WHERE sku = 'CASE-001'), (SELECT id FROM locations WHERE short_code = 'Z2' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH3')), 80, 75, NOW())
ON CONFLICT (product_id, location_id) DO UPDATE SET
    qty_on_hand = EXCLUDED.qty_on_hand,
    free_to_use = EXCLUDED.free_to_use,
    updated_at = EXCLUDED.updated_at;

-- 6. Insert Sample Operations (Receipts)
INSERT INTO operations (reference, operation_type, to_location_id, contact, schedule_date, status, created_at) VALUES
('WH1/IN/0001', 'IN', (SELECT id FROM locations WHERE short_code = 'A1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 'Supplier ABC', '2025-11-25', 'pending', NOW()),
('WH1/IN/0002', 'IN', (SELECT id FROM locations WHERE short_code = 'A2' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 'Supplier XYZ', '2025-11-20', 'pending', NOW()),
('WH1/IN/0003', 'IN', (SELECT id FROM locations WHERE short_code = 'CS1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 'Supplier DEF', '2025-12-01', 'pending', NOW()),
('WH2/IN/0001', 'IN', (SELECT id FROM locations WHERE short_code = 'SA1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH2')), 'Supplier GHI', '2025-11-18', 'pending', NOW()),
('WH3/IN/0001', 'IN', (SELECT id FROM locations WHERE short_code = 'Z1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH3')), 'Supplier JKL', '2025-11-30', 'pending', NOW())
ON CONFLICT (reference) DO NOTHING;

-- Insert Operation Lines for Receipts (Prices in Indian Rupees - ₹)
INSERT INTO operation_lines (operation_id, product_id, quantity, unit_cost) VALUES
-- WH1/IN/0001
((SELECT id FROM operations WHERE reference = 'WH1/IN/0001'), (SELECT id FROM products WHERE sku = 'LAP-001'), 10, 75149.17),
((SELECT id FROM operations WHERE reference = 'WH1/IN/0001'), (SELECT id FROM products WHERE sku = 'MSE-001'), 50, 2504.17),
-- WH1/IN/0002
((SELECT id FROM operations WHERE reference = 'WH1/IN/0002'), (SELECT id FROM products WHERE sku = 'MON-001'), 20, 25049.17),
((SELECT id FROM operations WHERE reference = 'WH1/IN/0002'), (SELECT id FROM products WHERE sku = 'CBL-001'), 100, 1084.67),
-- WH1/IN/0003
((SELECT id FROM operations WHERE reference = 'WH1/IN/0003'), (SELECT id FROM products WHERE sku = 'HP-001'), 15, 10854.17),
-- WH2/IN/0001
((SELECT id FROM operations WHERE reference = 'WH2/IN/0001'), (SELECT id FROM products WHERE sku = 'SSD-001'), 30, 7509.17),
((SELECT id FROM operations WHERE reference = 'WH2/IN/0001'), (SELECT id FROM products WHERE sku = 'RAM-001'), 50, 6679.17),
-- WH3/IN/0001
((SELECT id FROM operations WHERE reference = 'WH3/IN/0001'), (SELECT id FROM products WHERE sku = 'MB-001'), 10, 16699.17),
((SELECT id FROM operations WHERE reference = 'WH3/IN/0001'), (SELECT id FROM products WHERE sku = 'CPU-C-001'), 20, 4174.17);

-- 7. Insert Sample Operations (Deliveries)
INSERT INTO operations (reference, operation_type, from_location_id, contact, schedule_date, status, created_at) VALUES
('WH1/OUT/0001', 'OUT', (SELECT id FROM locations WHERE short_code = 'A1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 'Customer A', '2025-11-22', 'pending', NOW()),
('WH1/OUT/0002', 'OUT', (SELECT id FROM locations WHERE short_code = 'A2' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 'Customer B', '2025-11-19', 'pending', NOW()),
('WH2/OUT/0001', 'OUT', (SELECT id FROM locations WHERE short_code = 'SA1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH2')), 'Customer C', '2025-12-05', 'pending', NOW()),
('WH2/OUT/0002', 'OUT', (SELECT id FROM locations WHERE short_code = 'SB1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH2')), 'Customer D', '2025-11-28', 'pending', NOW())
ON CONFLICT (reference) DO NOTHING;

-- Insert Operation Lines for Deliveries (Prices in Indian Rupees - ₹)
INSERT INTO operation_lines (operation_id, product_id, quantity, unit_cost) VALUES
-- WH1/OUT/0001
((SELECT id FROM operations WHERE reference = 'WH1/OUT/0001'), (SELECT id FROM products WHERE sku = 'LAP-001'), 5, 75149.17),
((SELECT id FROM operations WHERE reference = 'WH1/OUT/0001'), (SELECT id FROM products WHERE sku = 'MSE-001'), 20, 2504.17),
-- WH1/OUT/0002
((SELECT id FROM operations WHERE reference = 'WH1/OUT/0002'), (SELECT id FROM products WHERE sku = 'MON-001'), 5, 25049.17),
((SELECT id FROM operations WHERE reference = 'WH1/OUT/0002'), (SELECT id FROM products WHERE sku = 'CBL-001'), 20, 1084.67),
-- WH2/OUT/0001
((SELECT id FROM operations WHERE reference = 'WH2/OUT/0001'), (SELECT id FROM products WHERE sku = 'SSD-001'), 10, 7509.17),
((SELECT id FROM operations WHERE reference = 'WH2/OUT/0001'), (SELECT id FROM products WHERE sku = 'RAM-001'), 20, 6679.17),
-- WH2/OUT/0002
((SELECT id FROM operations WHERE reference = 'WH2/OUT/0002'), (SELECT id FROM products WHERE sku = 'GPU-001'), 5, 33399.17),
((SELECT id FROM operations WHERE reference = 'WH2/OUT/0002'), (SELECT id FROM products WHERE sku = 'PSU-001'), 5, 7509.17);

-- 8. Insert Sample Operations (Adjustments - these are auto-validated)
INSERT INTO operations (reference, operation_type, to_location_id, contact, status, created_at, validated_at) VALUES
('WH1/ADJ/0001', 'ADJ', (SELECT id FROM locations WHERE short_code = 'A1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 'Inventory Count', 'validated', NOW(), NOW()),
('WH2/ADJ/0001', 'ADJ', (SELECT id FROM locations WHERE short_code = 'SA1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH2')), 'Inventory Count', 'validated', NOW(), NOW())
ON CONFLICT (reference) DO NOTHING;

-- Insert Operation Lines for Adjustments
INSERT INTO operation_lines (operation_id, product_id, quantity, unit_cost) VALUES
-- WH1/ADJ/0001
((SELECT id FROM operations WHERE reference = 'WH1/ADJ/0001'), (SELECT id FROM products WHERE sku = 'KBD-001'), 5, 6679.17),
-- WH2/ADJ/0001
((SELECT id FROM operations WHERE reference = 'WH2/ADJ/0001'), (SELECT id FROM products WHERE sku = 'SSD-001'), 10, 7509.17);

-- 9. Insert Sample Stock Ledger Entries (for Move History)
INSERT INTO stock_ledger (reference, date, product_id, from_location_id, to_location_id, quantity, operation_type, status, contact) VALUES
-- Validated Receipt
('WH1/IN/0001', NOW() - INTERVAL '5 days', (SELECT id FROM products WHERE sku = 'LAP-001'), NULL, (SELECT id FROM locations WHERE short_code = 'A1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 10, 'IN', 'validated', 'Supplier ABC'),
-- Validated Delivery
('WH1/OUT/0001', NOW() - INTERVAL '3 days', (SELECT id FROM products WHERE sku = 'LAP-001'), (SELECT id FROM locations WHERE short_code = 'A1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), NULL, 5, 'OUT', 'validated', 'Customer A'),
-- Adjustment
('WH1/ADJ/0001', NOW() - INTERVAL '2 days', (SELECT id FROM products WHERE sku = 'KBD-001'), NULL, (SELECT id FROM locations WHERE short_code = 'A1' AND warehouse_id = (SELECT id FROM warehouses WHERE short_code = 'WH1')), 5, 'ADJ', 'validated', 'Inventory Count');

-- Verify the data
SELECT 'Users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'Warehouses', COUNT(*) FROM warehouses
UNION ALL
SELECT 'Locations', COUNT(*) FROM locations
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'Stock Levels', COUNT(*) FROM stock_levels
UNION ALL
SELECT 'Operations', COUNT(*) FROM operations
UNION ALL
SELECT 'Operation Lines', COUNT(*) FROM operation_lines
UNION ALL
SELECT 'Stock Ledger', COUNT(*) FROM stock_ledger;

