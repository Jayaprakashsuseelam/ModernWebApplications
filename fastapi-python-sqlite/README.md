# HR Portal - Full Stack Application

A comprehensive HR management system built with **FastAPI (Backend)** and **React (Frontend)**, featuring a modern web interface for complete employee management.

## 🚀 Features

### Backend (FastAPI)
- **User Authentication**: JWT-based authentication with user registration and login
- **Employee Management**: Full CRUD operations for employee records
- **Role-based Access**: Admin and regular user roles with different permissions
- **RESTful API**: Clean, well-documented REST endpoints
- **SQLite Database**: Lightweight, file-based database
- **Auto-generated Documentation**: Interactive API docs with Swagger UI

### Frontend (React)
- **Modern UI/UX**: Bootstrap-based responsive design
- **Real-time Employee Management**: Create, view, edit, and delete employees
- **Advanced Filtering**: Filter employees by department and status
- **Employee Status Management**: Activate/deactivate employees with one click
- **Detailed Employee Views**: Modal popups with complete employee information
- **Form Validation**: Client-side validation with error handling
- **Loading States**: Visual feedback for all operations

## 📁 Project Structure

```
fastapi-python-sqlite/
│
├── Backend (FastAPI)
│   ├── main.py                  # FastAPI app entry point
│   ├── models.py                # SQLAlchemy models
│   ├── database.py              # DB connection & session
│   ├── auth.py                  # Login & JWT functions
│   ├── routers/
│   │   ├── users.py             # User registration/login
│   │   └── employees.py         # Employee CRUD endpoints
│   ├── requirements.txt         # Python dependencies
│   └── hr_portal.db            # SQLite database
│
└── Frontend (React)
    └── hr-portal-frontend/
        ├── src/
        │   ├── App.tsx          # Main React component
        │   ├── App.css          # Styles
        │   └── main.tsx         # React entry point
        ├── package.json         # Node.js dependencies
        ├── vite.config.ts       # Vite configuration
        └── index.html           # HTML template
```

## 🛠️ Setup Instructions

### Backend Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the FastAPI Server**
   ```bash
   # Option 1: Using uvicorn directly
   uvicorn main:app --reload

   # Option 2: Using Python
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to Frontend Directory**
   ```bash
   cd hr-portal-frontend
   ```

2. **Install Node.js Dependencies**
   ```bash
   npm install
   ```

3. **Start the Development Server**
   ```bash
   npm run dev
   ```

   The React app will be available at `http://localhost:5173`

## 🌐 Application Access

- **Frontend Application**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## 📋 API Endpoints

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

## 🎯 Frontend Features

### User Interface
- **Login/Registration**: Secure authentication with JWT tokens
- **Employee Dashboard**: Comprehensive employee management interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Clean, professional interface using Bootstrap

### Employee Management Features
- **📋 Employee Listing**: View all employees in a sortable table
- **🔍 Advanced Filtering**: Filter by department and active status
- **➕ Add New Employee**: Complete form with all employee fields
- **👁️ View Details**: Modal popup with complete employee information
- **✏️ Edit Employee**: Inline editing with pre-populated forms
- **🗑️ Delete Employee**: Secure deletion with confirmation
- **▶️/⏸️ Status Toggle**: Activate/deactivate employees instantly

### Data Fields
- Employee ID, First Name, Last Name
- Email, Phone, Address
- Department, Position, Hire Date
- Salary, Emergency Contact
- Active/Inactive Status
- Creation and Update Timestamps

## 🔧 Usage Examples

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

## 🔒 Security Notes

- **Change the SECRET_KEY**: In `auth.py`, replace the default secret key with a secure one
- **CORS Configuration**: Update CORS settings in `main.py` for production
- **Password Policy**: Implement stronger password requirements in production
- **Rate Limiting**: Add rate limiting for production use
- **Environment Variables**: Use environment variables for sensitive configuration

## 🗄️ Database

The application uses SQLite with the database file `hr_portal.db` created automatically in the project root. The database includes:

- **Users Table**: User accounts with authentication
- **Employees Table**: Complete employee records with timestamps

## 🚀 Development

### Adding New Models
1. Add the model to `models.py`
2. Run the application to create the table automatically
3. Create corresponding Pydantic models in the router
4. Add CRUD endpoints in the router
5. Update the frontend to include new fields

### Adding New Endpoints
1. Create a new router file in the `routers/` directory
2. Import and include the router in `main.py`
3. Follow the existing patterns for authentication and error handling
4. Update the frontend to consume new endpoints

### Frontend Development
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Bootstrap 5** for responsive UI components
- **Modern ES6+** JavaScript features

## 📦 Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **JWT**: JSON Web Tokens for authentication
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **React 18**: JavaScript library for building user interfaces
- **TypeScript**: Typed JavaScript for better development experience
- **Vite**: Fast build tool and development server
- **Bootstrap 5**: CSS framework for responsive design
- **Fetch API**: Modern HTTP client for API communication

## 📄 License

This project is open source and available under the MIT License. 