# Factories package for OOP Patient Management System
from .model_factory import (
    ModelFactory,
    PatientModelFactory,
    ModelFactoryRegistry,
    get_patient_factory,
    get_factory_registry,
    create_patient,
    create_adult_patient,
    create_minor_patient
)

__all__ = [
    'ModelFactory',
    'PatientModelFactory', 
    'ModelFactoryRegistry',
    'get_patient_factory',
    'get_factory_registry',
    'create_patient',
    'create_adult_patient',
    'create_minor_patient'
] 