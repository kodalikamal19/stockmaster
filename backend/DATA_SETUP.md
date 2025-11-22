# StockMaster - Sample Data Setup Guide

## Quick Setup

### Option 1: Use the SQL Script (Recommended)

1. Open **pgAdmin** and connect to your PostgreSQL database
2. Right-click on the `stockmaster1` database → **Query Tool**
3. Open the file `sample_data.sql` and copy all its contents
4. Paste into the Query Tool and click **Execute (F5)**
5. This will insert:
   - 2 Warehouses (WH1, WH2, WH3)
   - 8 Locations across warehouses
   - 15 Products (Laptops, Mice, Keyboards, etc.)
   - Stock levels for all products
   - Sample Receipts (pending)
   - Sample Deliveries (pending)
   - Sample Adjustments (validated)
   - Move history entries

### Option 2: Create Test User

**Before running the SQL script**, create a test user:

```bash
cd backend
python insert_test_user.py
```

This creates:
- **Login ID**: `admin001`
- **Email**: `admin@stockmaster.com`
- **Password**: `Password123!`

### Option 3: Sign Up via Web Interface

1. Start the frontend: `npm run dev` (in frontend folder)
2. Navigate to: `http://localhost:3000/signup`
3. Create your account

## What Data Gets Inserted?

### Warehouses
- **WH1**: Main Warehouse
- **WH2**: Secondary Warehouse  
- **WH3**: Distribution Center

### Locations
- **WH1**: Aisle 1, Aisle 2, Cold Storage, Loading Dock
- **WH2**: Section A, Section B
- **WH3**: Zone 1, Zone 2

### Products (15 items)
- Laptop Computer (LAP-001)
- Wireless Mouse (MSE-001)
- Keyboard Mechanical (KBD-001)
- Monitor 27 inch (MON-001)
- USB Cable Type-C (CBL-001)
- Webcam HD (CAM-001)
- Headphones Wireless (HP-001)
- External Hard Drive 1TB (HDD-001)
- SSD 500GB (SSD-001)
- RAM 16GB DDR4 (RAM-001)
- Graphics Card RTX 3060 (GPU-001)
- Power Supply 650W (PSU-001)
- Motherboard ATX (MB-001)
- CPU Cooler (CPU-C-001)
- Case Mid Tower (CASE-001)

### Operations
- **5 Pending Receipts** (you can validate these)
- **4 Pending Deliveries** (you can validate these)
- **2 Validated Adjustments** (already completed)

### Stock Levels
- Stock is distributed across different locations
- Each product has quantity on hand and free to use values

## Verify Data

After running the SQL script, you can verify by running this query in pgAdmin:

```sql
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
```

Expected counts:
- Users: 1+ (depending on if you created via script or signup)
- Warehouses: 3
- Locations: 8
- Products: 15
- Stock Levels: 15
- Operations: 11
- Operation Lines: 20+
- Stock Ledger: 3+

## Troubleshooting

### If you get foreign key errors:
- Make sure to run the INSERT statements in order (warehouses → locations → products → stock → operations)

### If users table is empty:
- Run `python insert_test_user.py` OR
- Create a user via the signup page

### To clear all data and start fresh:
```sql
TRUNCATE TABLE stock_ledger, operation_lines, operations, stock_levels, products, locations, warehouses, users CASCADE;
```
Then run the sample_data.sql script again.

