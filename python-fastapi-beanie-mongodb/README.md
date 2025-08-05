# Task Management System

A scalable Python application built with FastAPI, Beanie ODM, and MongoDB for efficient task management.

## Features

- **User Authentication & Authorization**: JWT-based authentication with role-based access control
- **Task Management**: Full CRUD operations for tasks with status tracking
- **User Management**: User registration, profile management, and role management
- **Task Assignment**: Assign tasks to users with priority levels
- **Statistics**: Task completion statistics and progress tracking
- **API Documentation**: Auto-generated OpenAPI documentation
- **Scalable Architecture**: Built with modern async/await patterns

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Beanie**: Asynchronous Python ODM for MongoDB
- **Motor**: Non-blocking MongoDB driver
- **PyMongo**: Official MongoDB Python driver
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **Uvicorn**: ASGI server for running FastAPI applications

## Project Structure

```
python-fastapi-beanie-mongodb/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Application configuration
│   │   ├── database.py        # Database connection
│   │   ├── deps.py           # Dependency injection
│   │   └── security.py       # Security utilities
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py           # User model
│   │   └── task.py           # Task model
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── users.py          # User management endpoints
│   │   └── tasks.py          # Task management endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py           # User Pydantic schemas
│   │   └── task.py           # Task Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py   # User business logic
│   │   └── task_service.py   # Task business logic
│   ├── utils/
│   ├── __init__.py
│   └── main.py               # FastAPI application
├── config.env                # Environment configuration
├── requirements.txt          # Python dependencies
├── run.py                   # Application startup script
└── README.md                # Project documentation
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python-fastapi-beanie-mongodb
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**
   - Install MongoDB locally or use MongoDB Atlas
   - Update `config.env` with your MongoDB connection string

4. **Configure environment**
   - Copy `config.env` and update with your settings
   - Update `SECRET_KEY` for production use

## Running the Application

### Development Mode
```bash
python run.py
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The application will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user info

### Users (Admin Only)
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user
- `PUT /api/v1/users/{user_id}/role` - Change user role

### Tasks
- `POST /api/v1/tasks/` - Create a new task
- `GET /api/v1/tasks/` - Get tasks (filtered by user role)
- `GET /api/v1/tasks/{task_id}` - Get task by ID
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task
- `PUT /api/v1/tasks/{task_id}/complete` - Mark task as completed
- `PUT /api/v1/tasks/{task_id}/assign/{user_id}` - Assign task to user
- `GET /api/v1/tasks/statistics/me` - Get user task statistics

## Usage Examples

### 1. Register a User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "password": "securepassword123"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### 3. Create a Task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive documentation for the new feature",
    "priority": "high",
    "due_date": "2024-02-01T00:00:00Z"
  }'
```

## Features in Detail

### Authentication & Authorization
- JWT-based authentication with configurable expiration
- Role-based access control (Admin/User)
- Password hashing with bcrypt
- Token-based session management

### Task Management
- Full CRUD operations for tasks
- Task status tracking (Pending, In Progress, Completed, Cancelled)
- Priority levels (Low, Medium, High, Urgent)
- Task assignment to users
- Due date management
- Completion tracking with timestamps

### User Management
- User registration and profile management
- Role-based permissions
- User statistics and activity tracking
- Admin-only user management features

### Data Models
- **User Model**: Email, username, password, role, timestamps
- **Task Model**: Title, description, status, priority, assignment, timestamps

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- Input validation with Pydantic
- CORS middleware for cross-origin requests

## Performance Features

- Asynchronous database operations
- Connection pooling with Motor
- Efficient querying with Beanie ODM
- Pagination for large datasets
- Optimized MongoDB queries

## Development

### Adding New Features
1. Create models in `app/models/`
2. Add Pydantic schemas in `app/schemas/`
3. Implement business logic in `app/services/`
4. Create API endpoints in `app/routers/`
5. Update dependencies in `app/core/deps.py`

### Testing
```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=app
```

### Code Quality
```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
```bash
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=task_management
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository. 