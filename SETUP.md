# StockMaster Setup Guide

## Complete Setup Instructions

### Option 1: Docker Setup (Recommended)

1. **Prerequisites**
   - Docker Desktop installed
   - Docker Compose installed

2. **Environment Configuration**
   - The application uses environment variables from `docker-compose.yml`
   - Default database credentials: `stockmaster` / `stockmaster123`
   - Default ports: Frontend (3000), Backend (5000), Database (5432)

3. **Start Services**
   ```bash
   docker-compose up -d
   ```

4. **Initialize Database**
   ```bash
   # Wait 10-15 seconds for PostgreSQL to be ready
   docker-compose exec api flask db init
   docker-compose exec api flask db migrate -m "Initial migration"
   docker-compose exec api flask db upgrade
   docker-compose exec api python seed_data.py
   ```

5. **Verify Setup**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:5000/api/docs
   - Login with: `admin` / `Admin123!`

### Option 2: Local Development Setup

#### Backend

1. **Install Python 3.10+**
   ```bash
   python --version  # Should be 3.10 or higher
   ```

2. **Create Virtual Environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up PostgreSQL**
   ```bash
   # Install PostgreSQL 15+
   # Create database
   createdb stockmaster
   # Or using psql:
   psql -U postgres
   CREATE DATABASE stockmaster;
   ```

5. **Configure Environment**
   Create `backend/.env`:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/stockmaster
   JWT_SECRET_KEY=your-secret-key-here
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=development
   ```

6. **Initialize Database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   python seed_data.py
   ```

7. **Run Backend**
   ```bash
   flask run
   # Or with auto-reload:
   flask run --reload
   ```

#### Frontend

1. **Install Node.js 18+**
   ```bash
   node --version  # Should be 18 or higher
   ```

2. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Configure Environment (Optional)**
   Create `frontend/.env`:
   ```env
   REACT_APP_API_URL=http://localhost:5000
   ```

4. **Run Frontend**
   ```bash
   npm run dev
   ```

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL is running
- Check database credentials in `.env` or `docker-compose.yml`
- Verify database exists: `psql -l | grep stockmaster`

### Port Conflicts

- Change ports in `docker-compose.yml` if 3000, 5000, or 5432 are in use
- Update `REACT_APP_API_URL` in frontend if backend port changes

### Migration Issues

- If migrations fail, you may need to drop and recreate:
  ```bash
  flask db downgrade base
  flask db upgrade
  ```

### Frontend Build Issues

- Clear node_modules and reinstall:
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```

## Production Deployment

1. **Environment Variables**
   - Set strong `JWT_SECRET_KEY` and `SECRET_KEY`
   - Use secure database credentials
   - Configure proper CORS origins

2. **Database**
   - Use managed PostgreSQL service
   - Set up regular backups
   - Configure connection pooling

3. **Security**
   - Enable HTTPS
   - Set up rate limiting
   - Configure firewall rules
   - Use environment variables for secrets

4. **Build Frontend**
   ```bash
   cd frontend
   npm run build
   # Serve static files with nginx or similar
   ```

5. **Backend**
   ```bash
   # Use gunicorn with multiple workers
   gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 run:app
   ```

## Development Tips

- Use Swagger docs at `/api/docs` for API testing
- Check logs: `docker-compose logs -f api`
- Run tests: `pytest` in backend directory
- Seed more data: Modify `seed_data.py` and rerun

