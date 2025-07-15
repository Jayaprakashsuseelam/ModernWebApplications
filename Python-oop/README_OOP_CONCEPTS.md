# 🏗️ Object-Oriented Programming Concepts Implementation

## 📋 **Overview**

This Patient Management System demonstrates comprehensive Object-Oriented Programming (OOP) concepts using Python. The project showcases real-world application of OOP principles with a complete architecture including models, services, factories, and design patterns.

## 🎯 **Core OOP Concepts Implemented**

### **1. 🔗 Inheritance**
**Definition**: A mechanism that allows a class to inherit properties and methods from another class.

**Implementation**:
```python
# Abstract Base Class
class BaseModel(ABC):
    def __init__(self, **kwargs):
        self._id = kwargs.get('id')
        # ... common attributes

# Concrete Class inheriting from Base
class Patient(BaseModel):
    def __init__(self, first_name, last_name, **kwargs):
        super().__init__(**kwargs)  # Call parent constructor
        self._first_name = first_name
        # ... patient-specific attributes
```

**Benefits**:
- ✅ Code re-usability
- ✅ Hierarchical organization
- ✅ Polymorphic behavior

### **2. 🔒 Encapsulation**
**Definition**: Bundling data and methods that operate on that data within a single unit (class) and restricting access to some of the object's components.

**Implementation**:
```python
class Patient(BaseModel):
    def __init__(self, first_name, last_name, **kwargs):
        # Private attributes (encapsulation)
        self._first_name = first_name
        self._last_name = last_name
        self._date_of_birth = date_of_birth
    
    # Public properties with validation (controlled access)
    @property
    def first_name(self) -> str:
        return self._first_name
    
    @first_name.setter
    def first_name(self, value: str):
        if not self._validate_name(value):
            raise ValueError("Invalid first name")
        self._first_name = value
    
    # Private validation method (hidden implementation)
    def _validate_name(self, name: str) -> bool:
        return bool(re.match(r"^[A-Za-z\s\-']{2,50}$", name.strip()))
```

**Benefits**:
- ✅ Data hiding
- ✅ Controlled access
- ✅ Validation enforcement

### **3. 🔄 Polymorphism**
**Definition**: The ability to present the same interface for different underlying forms (data types or classes).

**Implementation**:
```python
# Abstract method in base class
class BaseModel(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

# Different implementations in derived classes
class Patient(BaseModel):
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self._id,
            'first_name': self._first_name,
            'last_name': self._last_name,
            # ... patient-specific fields
        }

# Polymorphic usage
patients = [patient1, patient2, patient3]
patient_dicts = [p.to_dict() for p in patients]  # Same interface, different implementations
```

**Benefits**:
- ✅ Interface consistency
- ✅ Code flexibility
- ✅ Extensibility

### **4. 🎭 Abstraction**
**Definition**: Hiding complex implementation details and showing only necessary features.

**Implementation**:
```python
# Abstract base class
class BaseModel(ABC):
    @abstractmethod
    def validate(self) -> bool:
        """Validate model data - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def _get_insert_data(self) -> tuple[List[str], List[Any]]:
        """Get fields and values for INSERT - must be implemented by subclasses"""
        pass

# Concrete implementation hides complexity
class Patient(BaseModel):
    def validate(self) -> bool:
        # Complex validation logic hidden from users
        return (
            self._validate_name(self._first_name) and
            self._validate_date(self._date_of_birth) and
            self._validate_gender(self._gender) and
            self._validate_contact(self._contact_number)
        )
```

**Benefits**:
- ✅ Simplified interface
- ✅ Implementation hiding
- ✅ Focus on essential features

## 🏭 **Design Patterns Implemented**

### **1. Factory Pattern**
**Purpose**: Create objects without specifying their exact classes.

**Implementation**:
```python
class ModelFactory(ABC):
    @abstractmethod
    def create_model(self, model_type: str, **kwargs) -> BaseModel:
        pass

class PatientModelFactory(ModelFactory):
    def create_model(self, model_type: str, **kwargs) -> BaseModel:
        if model_type == 'patient':
            return Patient(**kwargs)
    
    def create_adult_patient(self, **kwargs) -> Patient:
        # Specialized factory method
        patient = Patient(**kwargs)
        if not patient.is_adult():
            raise ValueError("Patient must be 18 or older")
        return patient
```

### **2. Service Layer Pattern**
**Purpose**: Separate business logic from data access logic.

**Implementation**:
```python
class BaseService(ABC, Generic[T]):
    def __init__(self, model_class: type[T]):
        self._model_class = model_class
    
    def create(self, **kwargs) -> T:
        # Business logic here
        instance = self._model_class(**kwargs)
        instance.save()
        return instance

class PatientService(BaseService[Patient]):
    def get_statistics(self) -> Dict[str, Any]:
        # Complex business logic
        all_patients = self.get_all()
        adults = [p for p in all_patients if p.is_adult()]
        # ... statistical calculations
```

### **3. Singleton Pattern**
**Purpose**: Ensure a class has only one instance.

**Implementation**:
```python
class ModelFactoryRegistry:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._factories = {}
        return cls._instance
```

## 📁 **Project Structure**

```
Python-oop/
├── models/                     # Data Models (Inheritance)
│   ├── __init__.py
│   ├── base_model.py          # Abstract Base Class
│   └── patient.py             # Concrete Patient Model
├── services/                   # Business Logic (Service Layer)
│   ├── __init__.py
│   ├── base_service.py        # Abstract Service
│   └── patient_service.py     # Concrete Patient Service
├── factories/                  # Object Creation (Factory Pattern)
│   ├── __init__.py
│   └── model_factory.py       # Factory Implementation
├── web_app_oop.py             # Main Application
├── db.py                      # Database Connection
└── templates/
    └── index.html             # Frontend Interface
```

## 🚀 **How to Run the OOP Application**

### **1. Setup Environment**
```bash
# Activate virtual environment
source ../.venv/Scripts/activate

# Install dependencies
pip install Flask==2.3.3 psycopg2-binary python-dotenv
```

### **2. Configure Database**
```bash
# Create .env file
cp env_template.txt .env

# Edit .env with your PostgreSQL credentials
DB_NAME=hospital_db
DB_USER=hospitalUser
DB_PASSWORD=adminroot
DB_HOST=localhost
DB_PORT=5432
```

### **3. Run OOP Application**
```bash
python web_app_oop.py
```

### **4. Access OOP Features**
- **Main Interface**: http://localhost:5000
- **OOP Demo**: http://localhost:5000/api/oop/demo
- **Statistics**: http://localhost:5000/api/statistics
- **Factory Info**: http://localhost:5000/api/factory/registry

## 🔧 **OOP Features Demonstration**

### **1. Inheritance Demo**
```python
# BaseModel provides common functionality
patient = Patient(first_name="John", last_name="Doe", ...)
patient.save()  # Inherited from BaseModel
patient.delete()  # Inherited from BaseModel
```

### **2. Encapsulation Demo**
```python
# Private attributes with controlled access
patient.first_name = "Jane"  # Uses setter with validation
print(patient.first_name)    # Uses getter
# patient._first_name  # Direct access discouraged
```

### **3. Polymorphism Demo**
```python
# Same interface, different implementations
models = [patient1, patient2, patient3]
for model in models:
    print(model.to_dict())  # Polymorphic method call
```

### **4. Factory Pattern Demo**
```python
# Create objects without specifying exact class
factory = PatientModelFactory()
patient = factory.create_model('patient', **data)
adult_patient = factory.create_adult_patient(**data)
```

## 📊 **Advanced OOP Features**

### **1. Generic Types**
```python
class BaseService(ABC, Generic[T]):
    def __init__(self, model_class: type[T]):
        self._model_class = model_class
```

### **2. Magic Methods**
```python
def __str__(self) -> str:
    return f"Patient({self.get_full_name()}, ID: {self._id})"

def __eq__(self, other) -> bool:
    return self._id == other._id
```

### **3. Class Methods**
```python
@classmethod
def get_by_id(cls, patient_id: int) -> Optional['Patient']:
    # Factory method for creating instances
```

### **4. Property Decorators**
```python
@property
def age(self) -> Optional[int]:
    return self.get_age()

@age.setter
def age(self, value: int):
    # Cannot set age directly - calculated from date_of_birth
    raise AttributeError("Age is calculated from date of birth")
```

## 🎯 **OOP Benefits Demonstrated**

### **1. Code Reusability**
- BaseModel provides common CRUD operations
- BaseService provides common business logic
- Factory pattern reuses object creation logic

### **2. Maintainability**
- Clear separation of concerns
- Modular architecture
- Easy to extend and modify

### **3. Scalability**
- Easy to add new models (Doctor, Appointment, etc.)
- Service layer handles complex business logic
- Factory pattern supports multiple object types

### **4. Testability**
- Clear interfaces for mocking
- Separated concerns for unit testing
- Dependency injection support

## 🔍 **API Endpoints Demonstrating OOP**

| Endpoint | OOP Concept | Description |
|----------|-------------|-------------|
| `/api/patients` | Service Layer | CRUD operations through service |
| `/api/factory/create-adult` | Factory Pattern | Specialized object creation |
| `/api/patients/search/<name>` | Polymorphism | Same interface, different queries |
| `/api/statistics` | Encapsulation | Complex logic hidden behind simple interface |
| `/api/oop/demo` | All Concepts | Comprehensive OOP demonstration |

## 🏆 **Learning Outcomes**

This project demonstrates:

1. **Real-world OOP application** in a web application
2. **Design patterns** for scalable architecture
3. **Best practices** for object-oriented design
4. **Practical implementation** of abstract concepts
5. **Professional code structure** with proper separation of concerns

**The Patient Management System is now a comprehensive example of Object-Oriented Programming in action!** 🎉 