from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from datetime import datetime
import os

app = Flask(__name__)

# In-memory storage for patients
patients_db = []
next_id = 1

class Patient:
    def __init__(self, first_name, last_name, date_of_birth, gender, contact_number, id=None):
        global next_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.contact_number = contact_number
        self.id = id if id else next_id
        if not id:
            next_id += 1

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
        patients_db.append(self)
        return self

    @staticmethod
    def get_by_id(patient_id):
        for patient in patients_db:
            if patient.id == patient_id:
                return patient
        return None

    def update_contact(self, new_contact):
        self.contact_number = new_contact
        return self

    def delete(self):
        if self in patients_db:
            patients_db.remove(self)
            return True
        return False

    @staticmethod
    def get_all():
        return patients_db

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
    patient.first_name = data.get('first_name', patient.first_name)
    patient.last_name = data.get('last_name', patient.last_name)
    patient.date_of_birth = data.get('date_of_birth', patient.date_of_birth)
    patient.gender = data.get('gender', patient.gender)
    patient.contact_number = data.get('contact_number', patient.contact_number)
    
    return jsonify(patient.to_dict())

@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    if patient.delete():
        return jsonify({'message': 'Patient deleted successfully'})
    return jsonify({'error': 'Failed to delete patient'}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000) 