# Patient Management System - OOP Implementation

A comprehensive patient management system demonstrating **Object-Oriented Programming principles** with multiple implementation versions, from simple in-memory storage to full PostgreSQL database integration.

## 🎯 **Project Overview**

This project showcases **complete OOP implementation** with:
- ✅ **4 Core OOP Principles** (Inheritance, Encapsulation, Polymorphism, Abstraction)
- ✅ **4 Design Patterns** (Factory, Service Layer, Singleton, Registry)
- ✅ **Multiple Storage Options** (In-memory, PostgreSQL)
- ✅ **Professional Web Interface** (Flask + Bootstrap 5)
- ✅ **Comprehensive API** (RESTful endpoints with advanced queries)

## 🚀 **Quick Start - Choose Your Version**

### **1. 🧪 OOP Concepts Demo (No Setup Required)**
```bash
python oop_demo.py
```
**Perfect for**: Learning OOP concepts with live demonstrations

### **2. 💾 In-Memory Version (No Database Setup)**
```bash
python web_app.py
```
**Perfect for**: Quick testing and development

### **3. 🗄️ PostgreSQL Version (Persistent Storage)**
```bash
# Setup database
cp env_template.txt .env
# Edit .env with your PostgreSQL credentials

# Run application
python web_app_postgresql.py
```
**Perfect for**: Production-like environment with persistent data

### **4. 🏗️ Full OOP Version (Recommended)**
```bash
# Setup database
cp env_template.txt .env
# Edit .env with your PostgreSQL credentials

# Run OOP application
python web_app_oop.py
```
**Perfect for**: Complete OOP learning experience

## 🏗️ **Project Structure**

```
Python-oop/
├── models/                     # 🔗 OOP Models & Inheritance
│   ├── __init__.py
│   ├── base_model.py          # Abstract Base Class
│   └── patient.py             # Concrete Patient Model
├── services/                   # 🏭 Service Layer Pattern
│   ├── __init__.py
│   ├── base_service.py        # Abstract Service
│   └── patient_service.py     # Concrete Patient Service
├── factories/                  # 🏭 Factory Pattern
│   ├── __init__.py
│   └── model_factory.py       # Factory Implementation
├── web_app_oop.py             # 🌐 Main OOP Application
├── web_app_postgresql.py      # 🗄️ PostgreSQL Version
├── web_app.py                 # 💾 In-Memory Version
├── oop_demo.py                # 🧪 OOP Concepts Demo
├── check_db.py                # 🔍 Database Debug Tool
├── db.py                      # 🔌 Database Connection
├── templates/
│   └── index.html             # 🎨 Frontend Interface
├── README_OOP_CONCEPTS.md     # 📚 OOP Documentation
├── README_POSTGRESQL.md       # 🗄️ Database Documentation
├── requirements_postgresql.txt # 📦 Dependencies
└── env_template.txt           # ⚙️ Configuration Template
```

## 🎯 **OOP Concepts Demonstrated**

### **Core OOP Principles**
- **🔗 Inheritance**: `Patient` inherits from `BaseModel`
- **🔒 Encapsulation**: Private attributes with property decorators
- **🔄 Polymorphism**: Multiple `to_dict()` implementations
- **🎭 Abstraction**: Abstract base classes for models and services

### **Design Patterns**
- **🏭 Factory Pattern**: `PatientModelFactory` for object creation
- **🏭 Service Layer**: `PatientService` for business logic
- **🏭 Singleton**: `ModelFactoryRegistry` for single instance management
- **🏭 Registry**: Centralized factory registration

## 🌐 **Web Interface Features**

### **Modern UI Design**
- **Gradient Background**: Professional purple gradient theme
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Interactive Elements**: Hover effects, animations, and transitions
- **Color-Coded Data**: Gender badges, status indicators
- **Real-time Updates**: Dynamic content without page refresh

### **Patient Management**
- **Add Patients**: Form with validation and real-time feedback
- **View Patients**: Responsive table with sorting and filtering
- **Edit Patients**: Modal interface for quick updates
- **Delete Patients**: Confirmation dialogs for safety
- **Search & Filter**: Advanced query capabilities

## 📊 **Advanced API Endpoints**

### **Basic CRUD Operations**
- `GET /api/patients` - Get all patients
- `POST /api/patients` - Create new patient
- `GET /api/patients/<id>` - Get specific patient
- `PUT /api/patients/<id>` - Update patient
- `DELETE /api/patients/<id>` - Delete patient

### **Advanced Queries**
- `GET /api/patients/search/<name>` - Search by name
- `GET /api/patients/gender/<gender>` - Filter by gender
- `GET /api/patients/adults` - Get adult patients only
- `GET /api/patients/age-range/<min>/<max>` - Age range filtering
- `GET /api/patients/recent/<days>` - Recent patients
- `GET /api/patients/duplicates` - Find duplicate contacts

### **Analytics & Statistics**
- `GET /api/statistics` - Patient statistics
- `GET /api/patients/<id>/summary` - Patient summary
- `GET /api/status` - Database status
- `GET /api/oop/demo` - OOP concepts demonstration

## 🛠️ **Recent Fixes & Improvements**

### **✅ Database Schema Fix**
- **Issue**: Missing `created_at` column in PostgreSQL table
- **Solution**: Added `created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP` column
- **Result**: Patient data now displays correctly in web interface

### **✅ Enhanced Error Handling**
- Comprehensive error messages
- Database connection validation
- Data validation and sanitization
- Graceful error recovery

### **✅ Debug Tools**
- `check_db.py` - Database debugging and validation
- Connection testing utilities
- Schema validation tools

## 📋 **Patient Data Model**

Each patient record contains:
- **ID**: Unique identifier (auto-generated)
- **First Name**: Patient's first name (required)
- **Last Name**: Patient's last name (required)
- **Date of Birth**: Patient's birth date (required)
- **Gender**: Male, Female, or Other (required)
- **Contact Number**: Phone number (required)
- **Created At**: Timestamp of record creation (auto-generated)

## 🔧 **Installation & Setup**

### **Prerequisites**
- Python 3.7 or higher
- Virtual environment (recommended)
- PostgreSQL (for database versions)

### **Basic Setup**
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements_postgresql.txt
```

### **Database Setup (PostgreSQL Versions)**
```bash
# Copy environment template
cp env_template.txt .env

# Edit .env with your database credentials
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Create database and table (if needed)
# The application will create the table automatically
```

## 🎓 **Learning Resources**

### **Documentation**
- `README_OOP_CONCEPTS.md` - Detailed OOP concepts explanation
- `README_POSTGRESQL.md` - Database setup and configuration
- `PROJECT_SUMMARY.md` - Complete project overview

### **Demo Scripts**
- `oop_demo.py` - Live OOP concepts demonstration
- `check_db.py` - Database debugging and validation

### **Code Examples**
- Abstract base classes in `models/base_model.py`
- Factory pattern in `factories/model_factory.py`
- Service layer in `services/patient_service.py`
- Complete OOP application in `web_app_oop.py`

## 🏆 **Project Highlights**

### **✅ Educational Value**
- Complete OOP implementation
- Real-world application
- Professional architecture
- Comprehensive documentation

### **✅ Practical Application**
- Working web interface
- Database integration
- RESTful API design
- Modern UI/UX

### **✅ Scalable Design**
- Modular architecture
- Easy to extend
- Maintainable code
- Best practices

## 🎯 **Next Steps**

### **For Learning**
1. Run the OOP demo: `python oop_demo.py`
2. Study the code structure and patterns
3. Experiment with the web interface
4. Try adding new features

### **For Development**
1. Add new models (Doctor, Appointment, etc.)
2. Implement new services and factories
3. Create additional API endpoints
4. Extend the frontend interface

### **For Production**
1. Add user authentication
2. Implement comprehensive logging
3. Add unit and integration tests
4. Deploy to production environment

## 🎉 **Success!**

This project successfully demonstrates:
- **Complete OOP implementation** with all core principles
- **Real-world web application** with database integration
- **Professional architecture** using design patterns
- **Educational value** with comprehensive documentation
- **Working system** that can be extended and maintained

The Patient Management System is now fully functional with persistent PostgreSQL storage, comprehensive OOP architecture, and a beautiful web interface! 