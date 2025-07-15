from typing import List, Dict, Any, Optional
from datetime import datetime, date
from collections import Counter
from services.base_service import BaseService
from models.patient import Patient

class PatientService(BaseService[Patient]):
    """
    Patient Service implementing advanced OOP concepts:
    - Inheritance: Extends BaseService
    - Polymorphism: Custom implementations for patient-specific operations
    - Composition: Uses Patient model and additional business logic
    - Encapsulation: Private methods for complex operations
    """
    
    def __init__(self):
        """Initialize Patient Service"""
        super().__init__(Patient)
    
    # Polymorphism: Override base methods with patient-specific logic
    def create(self, **kwargs) -> Patient:
        """Create a new patient with validation"""
        if not self.validate_data(kwargs):
            raise ValueError("Invalid patient data")
        return super().create(**kwargs)
    
    def update(self, patient_id: int, **kwargs) -> Optional[Patient]:
        """Update patient with validation"""
        if not self.validate_data(kwargs):
            raise ValueError("Invalid patient data")
        return super().update(patient_id, **kwargs)
    
    # Abstract method implementations
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate patient data"""
        required_fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'contact_number']
        
        # Check required fields
        for field in required_fields:
            if field not in data or not data[field]:
                return False
        
        # Create temporary patient for validation
        try:
            temp_patient = Patient(**data)
            return temp_patient.validate()
        except:
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get patient statistics"""
        try:
            all_patients = self.get_all()
            
            # Calculate statistics
            total_patients = len(all_patients)
            adults = [p for p in all_patients if p.is_adult()]
            minors = [p for p in all_patients if not p.is_adult()]
            
            # Gender distribution
            gender_counts = Counter(p.gender.lower() for p in all_patients)
            
            # Age distribution
            ages = [p.get_age() for p in all_patients if p.get_age() is not None]
            avg_age = sum(ages) / len(ages) if ages else 0
            
            return {
                'total_patients': total_patients,
                'adults': len(adults),
                'minors': len(minors),
                'gender_distribution': dict(gender_counts),
                'average_age': round(avg_age, 1),
                'age_range': {
                    'min': min(ages) if ages else 0,
                    'max': max(ages) if ages else 0
                }
            }
        except Exception as e:
            return {'error': str(e)}
    
    # Patient-specific business logic methods
    def search_by_name(self, name: str) -> List[Patient]:
        """Search patients by name"""
        try:
            return Patient.search_by_name(name)
        except Exception as e:
            raise self._handle_error("search_by_name", e)
    
    def get_by_gender(self, gender: str) -> List[Patient]:
        """Get patients by gender"""
        try:
            return Patient.get_by_gender(gender)
        except Exception as e:
            raise self._handle_error("get_by_gender", e)
    
    def get_adults(self) -> List[Patient]:
        """Get all adult patients"""
        try:
            return Patient.get_adults()
        except Exception as e:
            raise self._handle_error("get_adults", e)
    
    def get_minors(self) -> List[Patient]:
        """Get all minor patients"""
        try:
            all_patients = self.get_all()
            return [p for p in all_patients if not p.is_adult()]
        except Exception as e:
            raise self._handle_error("get_minors", e)
    
    def get_by_age_range(self, min_age: int, max_age: int) -> List[Patient]:
        """Get patients within age range"""
        try:
            all_patients = self.get_all()
            return [
                p for p in all_patients 
                if p.get_age() is not None and min_age <= p.get_age() <= max_age
            ]
        except Exception as e:
            raise self._handle_error("get_by_age_range", e)
    
    def get_recent_patients(self, days: int = 30) -> List[Patient]:
        """Get patients created in the last N days"""
        try:
            all_patients = self.get_all()
            cutoff_date = datetime.now().date() - date.today().replace(day=days)
            
            return [
                p for p in all_patients 
                if p.created_at and p.created_at.date() >= cutoff_date
            ]
        except Exception as e:
            raise self._handle_error("get_recent_patients", e)
    
    def get_duplicate_contacts(self) -> List[List[Patient]]:
        """Find patients with duplicate contact numbers"""
        try:
            all_patients = self.get_all()
            contact_groups = {}
            
            for patient in all_patients:
                clean_contact = ''.join(filter(str.isdigit, patient.contact_number))
                if clean_contact in contact_groups:
                    contact_groups[clean_contact].append(patient)
                else:
                    contact_groups[clean_contact] = [patient]
            
            # Return only groups with duplicates
            return [group for group in contact_groups.values() if len(group) > 1]
        except Exception as e:
            raise self._handle_error("get_duplicate_contacts", e)
    
    def get_patients_without_contact(self) -> List[Patient]:
        """Get patients with invalid or missing contact numbers"""
        try:
            all_patients = self.get_all()
            return [
                p for p in all_patients 
                if not p._validate_contact(p.contact_number)
            ]
        except Exception as e:
            raise self._handle_error("get_patients_without_contact", e)
    
    def export_to_csv_format(self) -> List[Dict[str, Any]]:
        """Export patients to CSV format"""
        try:
            all_patients = self.get_all()
            csv_data = []
            
            for patient in all_patients:
                csv_data.append({
                    'ID': patient.id,
                    'First Name': patient.first_name,
                    'Last Name': patient.last_name,
                    'Full Name': patient.get_full_name(),
                    'Date of Birth': patient.date_of_birth,
                    'Age': patient.get_age(),
                    'Gender': patient.gender,
                    'Contact Number': patient.contact_number,
                    'Formatted Contact': patient.get_formatted_contact(),
                    'Is Adult': patient.is_adult(),
                    'Created At': str(patient.created_at) if patient.created_at else '',
                    'Updated At': str(patient.updated_at) if patient.updated_at else ''
                })
            
            return csv_data
        except Exception as e:
            raise self._handle_error("export_to_csv_format", e)
    
    def get_patient_summary(self, patient_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed patient summary"""
        try:
            patient = self.get_by_id(patient_id)
            if not patient:
                return None
            
            return {
                'basic_info': {
                    'id': patient.id,
                    'full_name': patient.get_full_name(),
                    'age': patient.get_age(),
                    'gender': patient.gender,
                    'contact': patient.get_formatted_contact()
                },
                'demographics': {
                    'is_adult': patient.is_adult(),
                    'age_group': self._get_age_group(patient.get_age()),
                    'contact_valid': patient._validate_contact(patient.contact_number)
                },
                'timestamps': {
                    'created_at': str(patient.created_at) if patient.created_at else None,
                    'updated_at': str(patient.updated_at) if patient.updated_at else None
                }
            }
        except Exception as e:
            raise self._handle_error("get_patient_summary", e)
    
    # Private helper methods (Encapsulation)
    def _get_age_group(self, age: Optional[int]) -> str:
        """Get age group category"""
        if age is None:
            return "Unknown"
        elif age < 18:
            return "Minor"
        elif age < 30:
            return "Young Adult"
        elif age < 50:
            return "Adult"
        elif age < 65:
            return "Middle-aged"
        else:
            return "Senior"
    
    def _validate_contact_format(self, contact: str) -> bool:
        """Validate contact number format"""
        import re
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', contact)
        return 7 <= len(digits_only) <= 15
    
    # Magic methods for better object representation
    def __str__(self) -> str:
        """String representation"""
        return f"PatientService(total_patients={len(self)})"
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        stats = self.get_statistics()
        return f"PatientService(total={stats.get('total_patients', 0)}, adults={stats.get('adults', 0)})" 