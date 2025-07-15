# Patient Management System with PostgreSQL

A modern web-based patient management system built with Python OOP principles, Flask, and PostgreSQL database.

## 🗄️ **Database: PostgreSQL**

This version uses **PostgreSQL** for persistent data storage, ensuring your patient data is safely stored and persists between application restarts.

## 🚀 **Features**

- **✅ Persistent Storage**: Data saved to PostgreSQL database
- **✅ CRUD Operations**: Create, Read, Update, Delete patients
- **✅ Modern UI**: Beautiful, responsive interface with Bootstrap 5
- **✅ Real-time Updates**: Dynamic content updates without page refresh
- **✅ Database Monitoring**: Built-in status and connection testing endpoints
- **✅ Error Handling**: Comprehensive error handling and logging
- **✅ OOP Design**: Clean object-oriented programming structure

## 📋 **Prerequisites**

### **1. PostgreSQL Database**
- PostgreSQL server installed and running
- A database created for the application
- Database user with appropriate permissions

### **2. Python Environment**
- Python 3.7 or higher
- Virtual environment (recommended)

## 🔧 **Setup Instructions**

### **Step 1: Install Dependencies**
```bash
# Activate virtual environment
source ../.venv/Scripts/activate  # Windows
# OR
source ../.venv/bin/activate      # macOS/Linux

# Install required packages
pip install Flask==2.3.3 psycopg2-binary python-dotenv
```

### **Step 2: Configure Database**

1. **Create a `.env` file** in the project directory:
```bash
# Copy the template
cp env_template.txt .env
```

2. **Edit the `.env` file** with your PostgreSQL credentials:
```env
DB_NAME=patient_management
DB_USER=postgres
DB_PASSWORD=your_actual_password
DB_HOST=localhost
DB_PORT=5432
```

3. **Create the database** in PostgreSQL:
```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database
CREATE DATABASE patient_management;

-- Create user (optional, if using different user)
CREATE USER patient_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE patient_management TO patient_user;
```

### **Step 3: Run the Application**
```bash
python web_app_postgresql.py
```

### **Step 4: Access the Application**
- **Main Interface**: http://localhost:5000
- **Database Status**: http://localhost:5000/api/status
- **Connection Test**: http://localhost:5000/api/test-connection

## 📊 **Database Schema**

The application automatically creates the following table:

```sql
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔌 **API Endpoints**

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/` | Main application interface | HTML page |
| `GET` | `/api/patients` | Get all patients | JSON array |
| `POST` | `/api/patients` | Create new patient | JSON object (201) |
| `GET` | `/api/patients/<id>` | Get specific patient | JSON object |
| `PUT` | `/api/patients/<id>` | Update patient | JSON object |
| `DELETE` | `/api/patients/<id>` | Delete patient | JSON message |
| `GET` | `/api/status` | Database status | JSON status |
| `GET` | `/api/test-connection` | Test PostgreSQL connection | JSON status |

## 🗂️ **File Structure**

```
Python-oop/
├── web_app_postgresql.py    # Main Flask application with PostgreSQL
├── db.py                   # Database connection module
├── models.py               # Original OOP Patient model
├── main.py                 # Original CLI application
├── templates/
│   └── index.html          # Frontend interface
├── .env                    # Database configuration (create this)
├── env_template.txt        # Environment template
└── README_POSTGRESQL.md    # This file
```

## 🔍 **Database Monitoring**

### **Check Database Status**
Visit: `http://localhost:5000/api/status`

**Response:**
```json
{
  "status": "connected",
  "database": "patient_management",
  "user": "postgres",
  "table_exists": true,
  "patient_count": 5
}
```

### **Test Database Connection**
Visit: `http://localhost:5000/api/test-connection`

**Response:**
```json
{
  "status": "success",
  "message": "PostgreSQL connection successful",
  "version": "PostgreSQL 14.5 on x86_64-pc-linux-gnu..."
}
```

## 🛠️ **Troubleshooting**

### **Connection Issues**
1. **Check PostgreSQL is running:**
   ```bash
   # Windows
   net start postgresql-x64-14
   
   # macOS/Linux
   sudo systemctl status postgresql
   ```

2. **Verify credentials in `.env` file**
3. **Check database exists:**
   ```sql
   \l  -- List databases
   ```

### **Permission Issues**
```sql
-- Grant permissions to user
GRANT ALL PRIVILEGES ON DATABASE patient_management TO your_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
```

### **Port Issues**
- **PostgreSQL default port**: 5432
- **Flask default port**: 5000
- Change ports in `.env` file if needed

## 📈 **Performance Features**

- **Connection Pooling**: Efficient database connections
- **Prepared Statements**: SQL injection protection
- **Transaction Management**: ACID compliance
- **Error Recovery**: Automatic rollback on errors
- **Connection Cleanup**: Proper resource management

## 🔒 **Security Features**

- **Environment Variables**: Secure credential storage
- **SQL Injection Protection**: Parameterized queries
- **Input Validation**: Frontend and backend validation
- **Error Handling**: No sensitive data in error messages

## 🚀 **Deployment**

### **Production Considerations**
1. **Use environment variables** for all sensitive data
2. **Set up proper PostgreSQL user permissions**
3. **Configure connection pooling** for high traffic
4. **Enable SSL** for database connections
5. **Set up regular backups**

### **Docker Deployment**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "web_app_postgresql.py"]
```

## 📝 **Example Usage**

### **Add a Patient via API**
```bash
curl -X POST http://localhost:5000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-05-15",
    "gender": "Male",
    "contact_number": "1234567890"
  }'
```

### **Get All Patients**
```bash
curl http://localhost:5000/api/patients
```

## 🎯 **Benefits of PostgreSQL Version**

- **✅ Data Persistence**: Data survives application restarts
- **✅ ACID Compliance**: Reliable transactions
- **✅ Scalability**: Handles large datasets efficiently
- **✅ Advanced Queries**: Complex data operations
- **✅ Backup & Recovery**: Professional database features
- **✅ Multi-user Support**: Concurrent access
- **✅ Data Integrity**: Constraints and validations

**Your patient data is now safely stored in PostgreSQL!** 🗄️✨ 