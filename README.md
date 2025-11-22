# StockMaster

A comprehensive full-stack web application for managing stock, warehouses, and operations.

## Features

- 🔐 **JWT Authentication** with email-based OTP for password reset
- 📊 **Dashboard** with real-time statistics for receipts and deliveries
- 📦 **Operations Management** (Receipts, Deliveries, Adjustments)
- 📈 **Stock Tracking** with search, sort, and filter capabilities
- 📜 **Move History** with color-coded inbound/outbound operations
- ⚙️ **Settings** for managing warehouses and locations
- 👤 **User Profile** management

## Tech Stack

### Backend
- Flask (Python)
- PostgreSQL
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Migrate

### Frontend
- React
- React Router
- Axios
- Vite

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

## Setup Instructions

### 1. Database Setup

Create a PostgreSQL database named `stockmaster1`:

```sql
CREATE DATABASE stockmaster1;
```

### 2. Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Update database credentials in `config.py` if needed (defaults are already set)

5. Initialize the database:
```bash
python app.py
```

This will create all necessary tables.

6. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### 3. Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## Database Configuration

The application uses the following PostgreSQL credentials (configured in `backend/config.py`):

- Host: localhost
- Port: 5432
- User: postgres
- Password: Kamal20*
- Database: stockmaster1

## Email Configuration

OTP emails are sent using Gmail SMTP (configured in `backend/config.py`):

- SMTP Server: smtp.gmail.com
- SMTP Port: 587
- Sender: kodalikamal1908@gmail.com

## API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/forgot-password` - Request OTP
- `POST /api/auth/verify-otp` - Verify OTP
- `POST /api/auth/reset-password` - Reset password

### Operations
- `GET /api/operations/receipts` - Get all receipts
- `POST /api/operations/receipts` - Create receipt
- `GET /api/operations/deliveries` - Get all deliveries
- `POST /api/operations/deliveries` - Create delivery
- `GET /api/operations/adjustments` - Get all adjustments
- `POST /api/operations/adjustments` - Create adjustment
- `GET /api/operations/:id` - Get operation details
- `POST /api/operations/:id/validate` - Validate operation
- `POST /api/operations/:id/cancel` - Cancel operation

### Stock
- `GET /api/stock` - Get stock levels

### Move History
- `GET /api/move-history` - Get move history

### Settings
- `GET /api/settings/warehouses` - Get warehouses
- `POST /api/settings/warehouses` - Create warehouse
- `PUT /api/settings/warehouses/:id` - Update warehouse
- `DELETE /api/settings/warehouses/:id` - Delete warehouse
- `GET /api/settings/locations` - Get locations
- `POST /api/settings/locations` - Create location
- `PUT /api/settings/locations/:id` - Update location
- `DELETE /api/settings/locations/:id` - Delete location

## Reference Format

Operations follow this reference format:
```
<WarehouseShortCode>/<OperationType>/<AutoIncrementID>
```

Example: `WH1/IN/0001`

## Project Structure

```
stockmaster1/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── requirements.txt
│   └── routes/
│       ├── auth.py
│       ├── dashboard.py
│       ├── locations.py
│       ├── move_history.py
│       ├── operations.py
│       ├── products.py
│       ├── profile.py
│       ├── settings.py
│       ├── stock.py
│       └── warehouses.py
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── components/
        ├── contexts/
        ├── pages/
        └── services/
```

## Usage

1. Start the backend server (port 5000)
2. Start the frontend server (port 3000)
3. Navigate to `http://localhost:3000`
4. Sign up for a new account or login
5. Start managing your stock!

## Notes

- All API endpoints require JWT authentication except signup, login, and password reset
- The application uses refresh tokens for automatic token renewal
- Stock levels are automatically updated when operations are validated
- Move history tracks all stock movements with color coding (green for inbound, red for outbound)

