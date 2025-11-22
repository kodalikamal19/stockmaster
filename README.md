# StockMaster

A modern, full-stack warehouse management system built with React, Flask, and PostgreSQL.

## Features

- 🔐 JWT Authentication with OTP password reset
- 📊 Interactive Dashboard with KPI cards
- 📦 Operations Management (Receipts, Deliveries, Adjustments)
- 📦 Stock Management with real-time tracking
- 📜 Move History with filtering and search
- ⚙️ Warehouse and Location Settings
- 👤 User Profile Management

## Tech Stack

- **Frontend**: React, React Query, React Router
- **Backend**: Flask, SQLAlchemy, Flask-JWT-Extended
- **Database**: PostgreSQL
- **DevOps**: Docker, Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose (for containerized setup)
- Node.js 18+ (for local frontend development)
- Python 3.10+ (for local backend development)
- PostgreSQL 15+ (for local database)

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd stockmaster
   ```

2. Create `.env` file in the root directory:
   ```bash
   # Copy and edit environment variables
   # See docker-compose.yml for default values
   ```

3. Start the application:
   ```bash
   docker-compose up -d
   ```

4. Initialize database and seed data:
   ```bash
   # Wait for services to be ready (about 10-15 seconds)
   docker-compose exec api flask db init
   docker-compose exec api flask db migrate -m "Initial migration"
   docker-compose exec api flask db upgrade
   docker-compose exec api python seed_data.py
   ```

5. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - API Docs: http://localhost:5000/api/docs

6. Default test credentials:
   - Login ID: `admin` / Password: `Admin123!`
   - Login ID: `testuser` / Password: `Test123!`

### Local Development

#### Backend Setup

1. Create virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   # Create .env file in backend/ directory
   # Add DATABASE_URL, JWT_SECRET_KEY, etc.
   ```

4. Set up PostgreSQL database:
   ```bash
   # Create database
   createdb stockmaster
   ```

5. Initialize and run migrations:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Seed data:
   ```bash
   python seed_data.py
   ```

7. Run the server:
   ```bash
   flask run
   # Or with gunicorn for production:
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

#### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Create `.env` file (optional):
   ```bash
   REACT_APP_API_URL=http://localhost:5000
   ```

3. Start development server:
   ```bash
   npm run dev
   # Or for production build:
   npm run build
   npm run preview
   ```

The frontend will be available at http://localhost:3000

## Project Structure

```
stockmaster/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   └── validators.py
│   ├── migrations/
│   ├── tests/
│   ├── requirements.txt
│   ├── seed_data.py
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── utils/
│   ├── public/
│   └── package.json
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

## API Documentation

Once the backend is running, visit http://localhost:5000/api/docs for interactive Swagger documentation.

## Testing

### Backend Tests

```bash
cd backend
pytest
# With coverage:
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm test
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/forgot-password` - Request password reset OTP
- `POST /api/auth/verify-otp` - Verify OTP
- `POST /api/auth/reset-password` - Reset password with OTP

### Operations
- `GET /api/operations/dashboard/stats` - Dashboard statistics
- `GET /api/operations/receipts` - List receipts
- `POST /api/operations/receipts` - Create receipt
- `GET /api/operations/deliveries` - List deliveries
- `POST /api/operations/deliveries` - Create delivery
- `GET /api/operations/adjustments` - List adjustments
- `POST /api/operations/adjustments` - Create adjustment
- `POST /api/operations/<id>/validate` - Validate operation
- `POST /api/operations/<id>/cancel` - Cancel operation

### Stock
- `GET /api/stock` - List stock with filters
- `GET /api/stock/<product_id>/<location_id>` - Get stock level
- `GET /api/stock/<product_id>/<location_id>/ledger` - Get stock ledger

### History
- `GET /api/history` - Get move history with filters

### Settings
- `GET /api/settings/warehouses` - List warehouses
- `POST /api/settings/warehouses` - Create warehouse
- `GET /api/settings/locations` - List locations
- `POST /api/settings/locations` - Create location

### Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile
- `POST /api/profile/logout` - Logout

For detailed API documentation, visit http://localhost:5000/api/docs when the backend is running.

## Environment Variables

See `.env.example` for required environment variables.

## License

MIT

