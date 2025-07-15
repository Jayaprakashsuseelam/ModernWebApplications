#!/usr/bin/env python3
"""
Object-Oriented Programming Concepts Demonstration
Patient Management System - OOP Implementation Showcase
"""

import sys
import os
from datetime import datetime, date

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.patient import Patient
from services.patient_service import PatientService
from factories.model_factory import (
    get_patient_factory, 
    get_factory_registry,
    create_patient,
    create_adult_patient,
    create_minor_patient
)

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"🏗️  {title}")
    print("="*60)

def print_section(title):
    """Print formatted section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def demo_inheritance():
    """Demonstrate Inheritance concept"""
    print_section("INHERITANCE DEMONSTRATION")
    
    print("1. Creating Patient instance (inherits from BaseModel):")
    patient = Patient(
        first_name="John",
        last_name="Doe",
        date_of_birth="1990-05-15",
        gender="Male",
        contact_number="1234567890"
    )
    
    print(f"   ✅ Patient created: {patient}")
    print(f"   📊 Patient ID: {patient.id}")
    print(f"   🕒 Created at: {patient.created_at}")
    
    print("\n2. Inherited methods from BaseModel:")
    print(f"   • to_dict(): {type(patient.to_dict())}")
    print(f"   • validate(): {patient.validate()}")
    print(f"   • __str__(): {str(patient)}")
    print(f"   • __repr__(): {repr(patient)}")

def demo_encapsulation():
    """Demonstrate Encapsulation concept"""
    print_section("ENCAPSULATION DEMONSTRATION")
    
    patient = Patient(
        first_name="Jane",
        last_name="Smith",
        date_of_birth="1985-03-20",
        gender="Female",
        contact_number="9876543210"
    )
    
    print("1. Private attributes with controlled access:")
    print(f"   • First Name: {patient.first_name} (using getter)")
    print(f"   • Last Name: {patient.last_name} (using getter)")
    
    print("\n2. Property setters with validation:")
    try:
        patient.first_name = "Mary"  # Valid name
        print(f"   ✅ Successfully set first_name to: {patient.first_name}")
    except ValueError as e:
        print(f"   ❌ Error: {e}")
    
    try:
        patient.first_name = "123"  # Invalid name
        print(f"   ✅ Successfully set first_name to: {patient.first_name}")
    except ValueError as e:
        print(f"   ❌ Validation error: {e}")
    
    print("\n3. Private methods (encapsulated implementation):")
    print(f"   • Full name: {patient.get_full_name()}")
    print(f"   • Age: {patient.get_age()}")
    print(f"   • Is adult: {patient.is_adult()}")

def demo_polymorphism():
    """Demonstrate Polymorphism concept"""
    print_section("POLYMORPHISM DEMONSTRATION")
    
    # Create multiple patients
    patients = [
        Patient(first_name="Alice", last_name="Johnson", date_of_birth="1992-08-10", gender="Female", contact_number="5551234567"),
        Patient(first_name="Bob", last_name="Brown", date_of_birth="1988-12-25", gender="Male", contact_number="5559876543"),
        Patient(first_name="Carol", last_name="Davis", date_of_birth="2000-04-15", gender="Female", contact_number="5554567890")
    ]
    
    print("1. Polymorphic method calls (same interface, different data):")
    for i, patient in enumerate(patients, 1):
        print(f"   Patient {i}: {patient.to_dict()}")
    
    print("\n2. Polymorphic property access:")
    for i, patient in enumerate(patients, 1):
        print(f"   Patient {i} full name: {patient.get_full_name()}")
    
    print("\3. Polymorphic validation:")
    for i, patient in enumerate(patients, 1):
        print(f"   Patient {i} validation: {patient.validate()}")

def demo_abstraction():
    """Demonstrate Abstraction concept"""
    print_section("ABSTRACTION DEMONSTRATION")
    
    patient = Patient(
        first_name="David",
        last_name="Wilson",
        date_of_birth="1975-11-30",
        gender="Male",
        contact_number="5557890123"
    )
    
    print("1. Complex validation hidden behind simple interface:")
    print(f"   • Patient validation: {patient.validate()}")
    print(f"   • Complex validation logic is hidden from user")
    
    print("\n2. Business logic abstraction:")
    print(f"   • Age calculation: {patient.get_age()}")
    print(f"   • Adult status: {patient.is_adult()}")
    print(f"   • Formatted contact: {patient.get_formatted_contact()}")
    
    print("\n3. Data transformation abstraction:")
    print(f"   • To dictionary: {type(patient.to_dict())}")
    print(f"   • To JSON: {type(patient.to_json())}")

def demo_factory_pattern():
    """Demonstrate Factory Pattern"""
    print_section("FACTORY PATTERN DEMONSTRATION")
    
    factory = get_patient_factory()
    
    print("1. Factory creates objects without specifying exact class:")
    patient_data = {
        'first_name': 'Emma',
        'last_name': 'Taylor',
        'date_of_birth': '1995-07-12',
        'gender': 'Female',
        'contact_number': '5553210987'
    }
    
    patient = factory.create_model('patient', **patient_data)
    print(f"   ✅ Created patient via factory: {patient.get_full_name()}")
    
    print("\n2. Specialized factory methods:")
    try:
        adult_patient = factory.create_adult_patient(**patient_data)
        print(f"   ✅ Created adult patient: {adult_patient.get_full_name()}")
    except ValueError as e:
        print(f"   ❌ Adult patient creation failed: {e}")
    
    try:
        minor_data = patient_data.copy()
        minor_data['date_of_birth'] = '2010-03-15'
        minor_patient = factory.create_minor_patient(**minor_data)
        print(f"   ✅ Created minor patient: {minor_patient.get_full_name()}")
    except ValueError as e:
        print(f"   ❌ Minor patient creation failed: {e}")

def demo_service_layer():
    """Demonstrate Service Layer Pattern"""
    print_section("SERVICE LAYER PATTERN DEMONSTRATION")
    
    service = PatientService()
    
    print("1. Service layer handles business logic:")
    print(f"   • Service type: {type(service)}")
    print(f"   • Service string representation: {service}")
    
    print("\n2. Service provides high-level operations:")
    # Note: These would require database connection in real usage
    print("   • create() - Creates and saves patient")
    print("   • get_all() - Retrieves all patients")
    print("   • get_statistics() - Calculates patient statistics")
    print("   • search_by_name() - Searches patients by name")
    
    print("\n3. Service encapsulates complex business rules:")
    print("   • Data validation")
    print("   • Business logic")
    print("   • Error handling")
    print("   • Transaction management")

def demo_singleton_pattern():
    """Demonstrate Singleton Pattern"""
    print_section("SINGLETON PATTERN DEMONSTRATION")
    
    registry1 = get_factory_registry()
    registry2 = get_factory_registry()
    
    print("1. Singleton ensures single instance:")
    print(f"   • Registry 1 ID: {id(registry1)}")
    print(f"   • Registry 2 ID: {id(registry2)}")
    print(f"   • Same instance: {registry1 is registry2}")
    
    print("\n2. Registry manages multiple factories:")
    factories = registry1.list_factories()
    print(f"   • Registered factories: {factories}")

def demo_advanced_oop_features():
    """Demonstrate Advanced OOP Features"""
    print_section("ADVANCED OOP FEATURES DEMONSTRATION")
    
    patient = Patient(
        first_name="Frank",
        last_name="Miller",
        date_of_birth="1982-09-18",
        gender="Male",
        contact_number="5556543210"
    )
    
    print("1. Magic Methods:")
    print(f"   • String representation: {str(patient)}")
    print(f"   • Detailed representation: {repr(patient)}")
    print(f"   • Hash value: {hash(patient)}")
    
    print("\n2. Property Decorators:")
    print(f"   • First name property: {patient.first_name}")
    print(f"   • Last name property: {patient.last_name}")
    
    print("\n3. Class Methods (demonstrated in Patient class):")
    print("   • get_by_id() - Factory method for creating instances")
    print("   • get_all() - Retrieves all instances")
    print("   • search_by_name() - Searches instances")
    
    print("\n4. Generic Types (in BaseService):")
    print("   • BaseService[Patient] - Type-safe service operations")
    print("   • Ensures type safety and better IDE support")

def demo_error_handling():
    """Demonstrate OOP Error Handling"""
    print_section("ERROR HANDLING DEMONSTRATION")
    
    print("1. Validation errors (encapsulation):")
    try:
        invalid_patient = Patient(
            first_name="",  # Invalid empty name
            last_name="Test",
            date_of_birth="1990-01-01",
            gender="Male",
            contact_number="123"
        )
    except ValueError as e:
        print(f"   ❌ Validation error caught: {e}")
    
    print("\n2. Factory validation errors:")
    try:
        factory = get_patient_factory()
        adult_data = {
            'first_name': 'Young',
            'last_name': 'Person',
            'date_of_birth': '2010-01-01',  # Too young for adult
            'gender': 'Male',
            'contact_number': '5551234567'
        }
        factory.create_adult_patient(**adult_data)
    except ValueError as e:
        print(f"   ❌ Factory validation error: {e}")

def main():
    """Main demonstration function"""
    print_header("OBJECT-ORIENTED PROGRAMMING CONCEPTS DEMONSTRATION")
    print("Patient Management System - Comprehensive OOP Implementation")
    
    try:
        # Demonstrate core OOP concepts
        demo_inheritance()
        demo_encapsulation()
        demo_polymorphism()
        demo_abstraction()
        
        # Demonstrate design patterns
        demo_factory_pattern()
        demo_service_layer()
        demo_singleton_pattern()
        
        # Demonstrate advanced features
        demo_advanced_oop_features()
        demo_error_handling()
        
        print_header("DEMONSTRATION COMPLETE")
        print("✅ All OOP concepts successfully demonstrated!")
        print("\n🎯 Key Takeaways:")
        print("   • Inheritance enables code reuse and hierarchy")
        print("   • Encapsulation protects data and enforces validation")
        print("   • Polymorphism provides flexible interfaces")
        print("   • Abstraction hides complexity from users")
        print("   • Design patterns solve common architectural problems")
        print("   • OOP creates maintainable and scalable code")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("Note: Some features require database connection for full functionality")

if __name__ == "__main__":
    main() 