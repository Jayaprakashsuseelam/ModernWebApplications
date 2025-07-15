from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)

# Database configuration
DATABASE = 'patients.db'

def init_db():
    """Initialize the database with the patients table"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create patients table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            gender TEXT NOT NULL,
            contact_number TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

class Patient:
    def __init__(self, first_name, last_name, date_of_birth, gender, contact_number, id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.contact_number = contact_number
        self.id = id

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'contact_number': self.contact_number
        }

    def save(self):
        """Save patient to database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patients (first_name, last_name, date_of_birth, gender, contact_number)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.first_name, self.last_name, self.date_of_birth, self.gender, self.contact_number))
        
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return self

    @staticmethod
    def get_by_id(patient_id):
        """Get patient by ID from database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Patient(
                first_name=row['first_name'],
                last_name=row['last_name'],
                date_of_birth=row['date_of_birth'],
                gender=row['gender'],
                contact_number=row['contact_number'],
                id=row['id']
            )
        return None

    def update(self, **kwargs):
        """Update patient in database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        update_fields = []
        values = []
        for field, value in kwargs.items():
            if hasattr(self, field) and value is not None:
                update_fields.append(f"{field} = ?")
                values.append(value)
                setattr(self, field, value)
        
        if update_fields:
            values.append(self.id)
            query = f"UPDATE patients SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
        return self

    def delete(self):
        """Delete patient from database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM patients WHERE id = ?', (self.id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted

    @staticmethod
    def get_all():
        """Get all patients from database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients ORDER BY id')
        rows = cursor.fetchall()
        conn.close()
        
        patients = []
        for row in rows:
            patient = Patient(
                first_name=row['first_name'],
                last_name=row['last_name'],
                date_of_birth=row['date_of_birth'],
                gender=row['gender'],
                contact_number=row['contact_number'],
                id=row['id']
            )
            patients.append(patient)
        
        return patients

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/patients', methods=['GET'])
def get_patients():
    patients = [patient.to_dict() for patient in Patient.get_all()]
    return jsonify(patients)

@app.route('/api/patients', methods=['POST'])
def create_patient():
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

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.get_by_id(patient_id)
    if patient:
        return jsonify(patient.to_dict())
    return jsonify({'error': 'Patient not found'}), 404

@app.route('/api/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
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

@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    if patient.delete():
        return jsonify({'message': 'Patient deleted successfully'})
    return jsonify({'error': 'Failed to delete patient'}), 500

@app.route('/api/status')
def status():
    """Check database status"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM patients')
        count = cursor.fetchone()[0]
        conn.close()
        return jsonify({
            'status': 'connected',
            'database': DATABASE,
            'patient_count': count
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    print(f"✅ Database initialized: {DATABASE}")
    print(f"📊 Database file location: {os.path.abspath(DATABASE)}")
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("🚀 Starting Flask application...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("📊 Check database status at: http://localhost:5000/api/status")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 