from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
from db import get_connection

# Import OOP components
from models.patient import Patient
from services.patient_service import PatientService
from factories.model_factory import get_patient_factory, get_factory_registry

app = Flask(__name__)

# Initialize services and factories (Dependency Injection)
patient_service = PatientService()
patient_factory = get_patient_factory()
factory_registry = get_factory_registry()

def init_db():
    """Initialize database with enhanced schema"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create patients table with additional columns for OOP features
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                date_of_birth DATE NOT NULL,
                gender VARCHAR(20) NOT NULL,
                contact_number VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        print("✅ OOP-enhanced database initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False
    finally:
        if conn:
            conn.close()

@app.route('/')
def index():
    """Main application interface"""
    return render_template('index.html')

# API Routes demonstrating OOP concepts
@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Get all patients using service layer"""
    try:
        patients = patient_service.get_all()
        return jsonify([patient.to_dict() for patient in patients])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients', methods=['POST'])
def create_patient():
    """Create patient using factory pattern and service layer"""
    try:
        data = request.json
        
        # Use factory pattern to create patient
        patient = patient_factory.create_patient_with_validation(**data)
        
        # Use service layer to save patient
        patient_service.create(**data)
        
        return jsonify(patient.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': f'Validation error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error creating patient: {str(e)}'}), 500

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient by ID using service layer"""
    try:
        patient = patient_service.get_by_id(patient_id)
        if patient:
            return jsonify(patient.to_dict())
        return jsonify({'error': 'Patient not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update patient using service layer"""
    try:
        data = request.json
        patient = patient_service.update(patient_id, **data)
        if patient:
            return jsonify(patient.to_dict())
        return jsonify({'error': 'Patient not found'}), 404
    except ValueError as e:
        return jsonify({'error': f'Validation error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete patient using service layer"""
    try:
        if patient_service.delete(patient_id):
            return jsonify({'message': 'Patient deleted successfully'})
        return jsonify({'error': 'Patient not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Advanced OOP Features API Routes
@app.route('/api/patients/search/<name>', methods=['GET'])
def search_patients(name):
    """Search patients by name using service layer"""
    try:
        patients = patient_service.search_by_name(name)
        return jsonify([patient.to_dict() for patient in patients])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/gender/<gender>', methods=['GET'])
def get_patients_by_gender(gender):
    """Get patients by gender using service layer"""
    try:
        patients = patient_service.get_by_gender(gender)
        return jsonify([patient.to_dict() for patient in patients])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/adults', methods=['GET'])
def get_adult_patients():
    """Get adult patients using service layer"""
    try:
        patients = patient_service.get_adults()
        return jsonify([patient.to_dict() for patient in patients])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/minors', methods=['GET'])
def get_minor_patients():
    """Get minor patients using service layer"""
    try:
        patients = patient_service.get_minors()
        return jsonify([patient.to_dict() for patient in patients])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/age-range/<int:min_age>/<int:max_age>', methods=['GET'])
def get_patients_by_age_range(min_age, max_age):
    """Get patients by age range using service layer"""
    try:
        patients = patient_service.get_by_age_range(min_age, max_age)
        return jsonify([patient.to_dict() for patient in patients])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/recent/<int:days>', methods=['GET'])
def get_recent_patients(days):
    """Get recent patients using service layer"""
    try:
        patients = patient_service.get_recent_patients(days)
        return jsonify([patient.to_dict() for patient in patients])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/duplicates', methods=['GET'])
def get_duplicate_contacts():
    """Get patients with duplicate contacts using service layer"""
    try:
        duplicate_groups = patient_service.get_duplicate_contacts()
        result = []
        for group in duplicate_groups:
            result.append([patient.to_dict() for patient in group])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/invalid-contacts', methods=['GET'])
def get_patients_without_contact():
    """Get patients with invalid contacts using service layer"""
    try:
        patients = patient_service.get_patients_without_contact()
        return jsonify([patient.to_dict() for patient in patients])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>/summary', methods=['GET'])
def get_patient_summary(patient_id):
    """Get detailed patient summary using service layer"""
    try:
        summary = patient_service.get_patient_summary(patient_id)
        if summary:
            return jsonify(summary)
        return jsonify({'error': 'Patient not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get patient statistics using service layer"""
    try:
        stats = patient_service.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/csv', methods=['GET'])
def export_to_csv():
    """Export patients to CSV format using service layer"""
    try:
        csv_data = patient_service.export_to_csv_format()
        return jsonify(csv_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Factory Pattern API Routes
@app.route('/api/factory/create-adult', methods=['POST'])
def create_adult_patient():
    """Create adult patient using factory pattern"""
    try:
        data = request.json
        patient = patient_factory.create_adult_patient(**data)
        patient.save()
        return jsonify(patient.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': f'Validation error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/factory/create-minor', methods=['POST'])
def create_minor_patient():
    """Create minor patient using factory pattern"""
    try:
        data = request.json
        patient = patient_factory.create_minor_patient(**data)
        patient.save()
        return jsonify(patient.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': f'Validation error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/factory/supported-models', methods=['GET'])
def get_supported_models():
    """Get supported model types from factory"""
    try:
        models = patient_factory.get_supported_models()
        return jsonify({'supported_models': models})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/factory/registry', methods=['GET'])
def get_factory_registry_info():
    """Get factory registry information"""
    try:
        factories = factory_registry.list_factories()
        return jsonify({
            'registered_factories': factories,
            'registry_type': 'Singleton Pattern'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# OOP Concepts Demonstration Routes
@app.route('/api/oop/demo', methods=['GET'])
def oop_demo():
    """Demonstrate OOP concepts"""
    try:
        # Create sample patients using different OOP patterns
        sample_data = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': '1990-05-15',
                'gender': 'Male',
                'contact_number': '1234567890'
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'date_of_birth': '2005-03-20',
                'gender': 'Female',
                'contact_number': '9876543210'
            }
        ]
        
        # Demonstrate Factory Pattern
        factory_patient = patient_factory.create_patient_from_dict(sample_data[0])
        
        # Demonstrate Service Layer
        service_patient = patient_service.create(**sample_data[1])
        
        # Demonstrate Polymorphism
        patients = [factory_patient, service_patient]
        patient_dicts = [p.to_dict() for p in patients]  # Polymorphic to_dict() calls
        
        # Demonstrate Encapsulation
        full_names = [p.get_full_name() for p in patients]  # Encapsulated method calls
        
        # Demonstrate Inheritance
        base_methods = ['save', 'delete', 'validate']  # Inherited from BaseModel
        
        return jsonify({
            'oop_concepts_demonstrated': {
                'inheritance': 'Patient extends BaseModel',
                'encapsulation': 'Private attributes with public properties',
                'polymorphism': 'Different implementations of to_dict()',
                'abstraction': 'Abstract BaseModel with concrete Patient implementation',
                'factory_pattern': 'PatientModelFactory creates Patient objects',
                'service_layer': 'PatientService handles business logic',
                'singleton_pattern': 'ModelFactoryRegistry ensures single instance'
            },
            'sample_patients': patient_dicts,
            'full_names': full_names,
            'inherited_methods': base_methods,
            'total_patients': len(patient_service)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Check application and database status"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check database connection
        cursor.execute('SELECT version()')
        version = cursor.fetchone()[0]
        
        # Check patients table
        cursor.execute('SELECT COUNT(*) FROM patients')
        patient_count = cursor.fetchone()[0]
        
        # Get database info
        cursor.execute('SELECT current_database(), current_user')
        db_info = cursor.fetchone()
        
        conn.close()
        
        return jsonify({
            'status': 'operational',
            'database': {
                'name': db_info[0],
                'user': db_info[1],
                'version': version,
                'patient_count': patient_count
            },
            'oop_architecture': {
                'models': 'BaseModel (Abstract) -> Patient (Concrete)',
                'services': 'BaseService (Abstract) -> PatientService (Concrete)',
                'factories': 'ModelFactory (Abstract) -> PatientModelFactory (Concrete)',
                'patterns': ['Factory Pattern', 'Service Layer', 'Singleton', 'Registry']
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Patient Management System with OOP Architecture...")
    
    # Test database connection
    print("🔍 Testing database connection...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT version()')
        version = cursor.fetchone()[0]
        conn.close()
        print(f"✅ Database connected: {version}")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        exit(1)
    
    # Initialize database
    print("🔧 Initializing OOP-enhanced database...")
    if not init_db():
        print("❌ Database initialization failed!")
        exit(1)
    
    # Create templates directory
    os.makedirs('templates', exist_ok=True)
    
    print("\n🎉 OOP Patient Management System Ready!")
    print("🌐 Main Interface: http://localhost:5000")
    print("📊 Status: http://localhost:5000/api/status")
    print("🧪 OOP Demo: http://localhost:5000/api/oop/demo")
    print("📈 Statistics: http://localhost:5000/api/statistics")
    print("\n🏗️ OOP Architecture Features:")
    print("   • Inheritance: BaseModel -> Patient")
    print("   • Encapsulation: Private attributes with properties")
    print("   • Polymorphism: Multiple implementations")
    print("   • Abstraction: Abstract base classes")
    print("   • Factory Pattern: Object creation")
    print("   • Service Layer: Business logic separation")
    print("   • Singleton Pattern: Registry management")
    print("\n" + "="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 