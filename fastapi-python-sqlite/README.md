# HR Portal API

A comprehensive HR management system built with FastAPI, Python, and SQLite.

## Features

- **User Authentication**: JWT-based authentication with user registration and login
- **Employee Management**: Full CRUD operations for employee records
- **Role-based Access**: Admin and regular user roles with different permissions
- **RESTful API**: Clean, well-documented REST endpoints
- **SQLite Database**: Lightweight, file-based database
- **Auto-generated Documentation**: Interactive API docs with Swagger UI

## Project Structure

```
hr-portal/
│
├── main.py                  # FastAPI app entry point
├── models.py                # SQLAlchemy models
├── database.py              # DB connection & session
├── auth.py                  # Login & JWT functions
├── routers/
│   ├── users.py             # User registration/login
│   └── employees.py         # Employee CRUD endpoints
└── requirements.txt         # Dependencies
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
# Option 1: Using uvicorn directly
uvicorn main:app --reload

# Option 2: Using Python
python main.py
```

The API will be available at `http://localhost:8000`

### 3. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /users/register` - Register a new user
- `POST /users/login` - Login and get JWT token
- `GET /users/me` - Get current user info
- `GET /users/` - List all users (admin only)

### Employee Management

- `POST /employees/` - Create a new employee
- `GET /employees/` - List employees (with optional filters)
- `GET /employees/{employee_id}` - Get specific employee
- `PUT /employees/{employee_id}` - Update employee
- `DELETE /employees/{employee_id}` - Delete employee (admin only)
- `PATCH /employees/{employee_id}/activate` - Activate employee
- `PATCH /employees/{employee_id}/deactivate` - Deactivate employee

### System

- `GET /` - API welcome message
- `GET /health` - Health check
- `GET /db-test` - Database connection test

## Usage Examples

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/users/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@company.com",
       "username": "admin",
       "password": "admin123",
       "full_name": "Admin User",
       "is_admin": true
     }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/users/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
```

### 3. Create an Employee (with authentication)

```bash
curl -X POST "http://localhost:8000/employees/" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "employee_id": "EMP001",
       "first_name": "John",
       "last_name": "Doe",
       "email": "john.doe@company.com",
       "phone": "+1234567890",
       "department": "Engineering",
       "position": "Software Engineer",
       "hire_date": "2023-01-15T00:00:00",
       "salary": 75000,
       "address": "123 Main St, City, State",
       "emergency_contact": "+1987654321"
     }'
```

## Security Notes

- **Change the SECRET_KEY**: In `auth.py`, replace the default secret key with a secure one
- **CORS Configuration**: Update CORS settings in `main.py` for production
- **Password Policy**: Implement stronger password requirements in production
- **Rate Limiting**: Add rate limiting for production use

## Database

The application uses SQLite with the database file `hr_portal.db` created automatically in the project root.

## Development

### Adding New Models

1. Add the model to `models.py`
2. Run the application to create the table automatically
3. Create corresponding Pydantic models in the router
4. Add CRUD endpoints in the router

### Adding New Endpoints

1. Create a new router file in the `routers/` directory
2. Import and include the router in `main.py`
3. Follow the existing patterns for authentication and error handling

## License

This project is open source and available under the MIT License. 