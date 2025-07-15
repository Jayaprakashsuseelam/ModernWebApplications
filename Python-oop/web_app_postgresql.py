from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from datetime import datetime
import os
from db import get_connection

app = Flask(__name__)

def init_db():
    """Initialize the database with the patients table"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create patients table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                date_of_birth DATE NOT NULL,
                gender VARCHAR(20) NOT NULL,
                contact_number VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        print("✅ PostgreSQL table 'patients' created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        return False
    finally:
        if conn:
            conn.close()

class Patient:
    def __init__(self, first_name, last_name, date_of_birth, gender, contact_number, id=None, created_at=None):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.contact_number = contact_number
        self.id = id
        self.created_at = created_at

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': str(self.date_of_birth) if self.date_of_birth else None,
            'gender': self.gender,
            'contact_number': self.contact_number,
            'created_at': str(self.created_at) if self.created_at else None
        }

    def save(self):
        """Save patient to PostgreSQL database"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO patients (first_name, last_name, date_of_birth, gender, contact_number)
                VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at
            ''', (self.first_name, self.last_name, self.date_of_birth, self.gender, self.contact_number))
            
            result = cursor.fetchone()
            self.id = result[0]
            self.created_at = result[1]
            
            conn.commit()
            print(f"✅ Patient saved with ID: {self.id}")
            return self
        except Exception as e:
            print(f"❌ Error saving patient: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(patient_id):
        """Get patient by ID from PostgreSQL database"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM patients WHERE id = %s', (patient_id,))
            row = cursor.fetchone()
            
            if row:
                return Patient(
                    first_name=row[1],
                    last_name=row[2],
                    date_of_birth=row[3],
                    gender=row[4],
                    contact_number=row[5],
                    id=row[0],
                    created_at=row[6]
                )
            return None
        except Exception as e:
            print(f"❌ Error getting patient by ID: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def update(self, **kwargs):
        """Update patient in PostgreSQL database"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Build dynamic update query
            update_fields = []
            values = []
            for field, value in kwargs.items():
                if hasattr(self, field) and value is not None:
                    update_fields.append(f"{field} = %s")
                    values.append(value)
                    setattr(self, field, value)
            
            if update_fields:
                values.append(self.id)
                query = f"UPDATE patients SET {', '.join(update_fields)} WHERE id = %s"
                cursor.execute(query, values)
                conn.commit()
                print(f"✅ Patient {self.id} updated successfully")
            
            return self
        except Exception as e:
            print(f"❌ Error updating patient: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def delete(self):
        """Delete patient from PostgreSQL database"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM patients WHERE id = %s', (self.id,))
            deleted = cursor.rowcount > 0
            conn.commit()
            
            if deleted:
                print(f"✅ Patient {self.id} deleted successfully")
            else:
                print(f"❌ Patient {self.id} not found for deletion")
            
            return deleted
        except Exception as e:
            print(f"❌ Error deleting patient: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_all():
        """Get all patients from PostgreSQL database"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM patients ORDER BY id')
            rows = cursor.fetchall()
            
            patients = []
            for row in rows:
                patient = Patient(
                    first_name=row[1],
                    last_name=row[2],
                    date_of_birth=row[3],
                    gender=row[4],
                    contact_number=row[5],
                    id=row[0],
                    created_at=row[6]
                )
                patients.append(patient)
            
            return patients
        except Exception as e:
            print(f"❌ Error getting all patients: {e}")
            return []
        finally:
            if conn:
                conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/patients', methods=['GET'])
def get_patients():
    patients = [patient.to_dict() for patient in Patient.get_all()]
    return jsonify(patients)

@app.route('/api/patients', methods=['POST'])
def create_patient():
    try:
        data = request.json
        patient = Patient(
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data['date_of_birth'],
            gender=data['gender'],
            contact_number=data['contact_number']
        )
        patient.save()
        return jsonify(patient.to_dict()), 201
    except Exception as e:
        return jsonify({'error': f'Failed to create patient: {str(e)}'}), 500

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.get_by_id(patient_id)
    if patient:
        return jsonify(patient.to_dict())
    return jsonify({'error': 'Patient not found'}), 404

@app.route('/api/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    try:
        patient = Patient.get_by_id(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        data = request.json
        patient.update(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            date_of_birth=data.get('date_of_birth'),
            gender=data.get('gender'),
            contact_number=data.get('contact_number')
        )
        
        return jsonify(patient.to_dict())
    except Exception as e:
        return jsonify({'error': f'Failed to update patient: {str(e)}'}), 500

@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    try:
        patient = Patient.get_by_id(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        if patient.delete():
            return jsonify({'message': 'Patient deleted successfully'})
        return jsonify({'error': 'Failed to delete patient'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to delete patient: {str(e)}'}), 500

@app.route('/api/status')
def status():
    """Check PostgreSQL database status"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute('''
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'patients'
            )
        ''')
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            cursor.execute('SELECT COUNT(*) FROM patients')
            count = cursor.fetchone()[0]
        else:
            count = 0
        
        # Get database info
        cursor.execute('SELECT current_database(), current_user')
        db_info = cursor.fetchone()
        
        conn.close()
        
        return jsonify({
            'status': 'connected',
            'database': db_info[0],
            'user': db_info[1],
            'table_exists': table_exists,
            'patient_count': count
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/test-connection')
def test_connection():
    """Test PostgreSQL connection"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT version()')
        version = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'PostgreSQL connection successful',
            'version': version
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'PostgreSQL connection failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Patient Management System with PostgreSQL...")
    
    # Test database connection first
    print("🔍 Testing PostgreSQL connection...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT version()')
        version = cursor.fetchone()[0]
        conn.close()
        print(f"✅ PostgreSQL connected successfully!")
        print(f"📊 Database version: {version}")
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        print("💡 Make sure your .env file has the correct database credentials:")
        print("   DB_NAME=your_database_name")
        print("   DB_USER=your_username")
        print("   DB_PASSWORD=your_password")
        print("   DB_HOST=localhost")
        print("   DB_PORT=5432")
        exit(1)
    
    # Initialize database
    print("🔧 Initializing database...")
    if init_db():
        print("✅ Database initialization completed!")
    else:
        print("❌ Database initialization failed!")
        exit(1)
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("\n🎉 Application ready!")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("📊 Check database status at: http://localhost:5000/api/status")
    print("🔍 Test connection at: http://localhost:5000/api/test-connection")
    print("\n" + "="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 