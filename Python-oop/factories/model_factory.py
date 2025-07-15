from abc import ABC, abstractmethod
from typing import Dict, Any, Type, Optional
from models.base_model import BaseModel
from models.patient import Patient

class ModelFactory(ABC):
    """
    Abstract Factory implementing Factory Pattern:
    - Factory Pattern: Creates objects without specifying exact classes
    - Abstraction: Abstract factory interface
    - Polymorphism: Different factory implementations
    """
    
    @abstractmethod
    def create_model(self, model_type: str, **kwargs) -> BaseModel:
        """Create a model instance"""
        pass
    
    @abstractmethod
    def get_supported_models(self) -> list[str]:
        """Get list of supported model types"""
        pass

class PatientModelFactory(ModelFactory):
    """
    Concrete Factory for Patient models:
    - Inheritance: Extends ModelFactory
    - Polymorphism: Implements abstract methods
    - Encapsulation: Private factory methods
    """
    
    def __init__(self):
        """Initialize factory with supported models"""
        self._supported_models = ['patient']
        self._model_classes = {
            'patient': Patient
        }
    
    def create_model(self, model_type: str, **kwargs) -> BaseModel:
        """Create a patient model instance"""
        if model_type not in self._supported_models:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        model_class = self._model_classes[model_type]
        return model_class(**kwargs)
    
    def get_supported_models(self) -> list[str]:
        """Get supported model types"""
        return self._supported_models.copy()
    
    # Factory methods for specific patient types
    def create_adult_patient(self, **kwargs) -> Patient:
        """Create an adult patient (18+)"""
        # Validate age
        if 'date_of_birth' in kwargs:
            temp_patient = Patient(**kwargs)
            if not temp_patient.is_adult():
                raise ValueError("Patient must be 18 or older")
        return self.create_model('patient', **kwargs)
    
    def create_minor_patient(self, **kwargs) -> Patient:
        """Create a minor patient (<18)"""
        # Validate age
        if 'date_of_birth' in kwargs:
            temp_patient = Patient(**kwargs)
            if temp_patient.is_adult():
                raise ValueError("Patient must be under 18")
        return self.create_model('patient', **kwargs)
    
    def create_patient_from_dict(self, data: Dict[str, Any]) -> Patient:
        """Create patient from dictionary data"""
        return self.create_model('patient', **data)
    
    def create_patient_with_validation(self, **kwargs) -> Patient:
        """Create patient with enhanced validation"""
        # Additional validation logic
        if 'contact_number' in kwargs:
            contact = kwargs['contact_number']
            if not self._validate_contact_format(contact):
                raise ValueError("Invalid contact number format")
        
        return self.create_model('patient', **kwargs)
    
    # Private helper methods
    def _validate_contact_format(self, contact: str) -> bool:
        """Validate contact number format"""
        import re
        digits_only = re.sub(r'\D', '', contact)
        return 7 <= len(digits_only) <= 15

class ModelFactoryRegistry:
    """
    Registry pattern for managing multiple factories:
    - Singleton Pattern: Single registry instance
    - Registry Pattern: Centralized factory management
    - Dependency Injection: Factory injection
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._factories = {}
            cls._instance._initialize_default_factories()
        return cls._instance
    
    def _initialize_default_factories(self):
        """Initialize default factories"""
        self.register_factory('patient', PatientModelFactory())
    
    def register_factory(self, name: str, factory: ModelFactory):
        """Register a factory"""
        self._factories[name] = factory
    
    def get_factory(self, name: str) -> Optional[ModelFactory]:
        """Get factory by name"""
        return self._factories.get(name)
    
    def create_model(self, factory_name: str, model_type: str, **kwargs) -> BaseModel:
        """Create model using registered factory"""
        factory = self.get_factory(factory_name)
        if not factory:
            raise ValueError(f"Factory not found: {factory_name}")
        return factory.create_model(model_type, **kwargs)
    
    def list_factories(self) -> list[str]:
        """List all registered factories"""
        return list(self._factories.keys())

# Utility functions for easy factory access
def get_patient_factory() -> PatientModelFactory:
    """Get patient factory instance"""
    return PatientModelFactory()

def get_factory_registry() -> ModelFactoryRegistry:
    """Get factory registry instance"""
    return ModelFactoryRegistry()

def create_patient(**kwargs) -> Patient:
    """Convenience function to create a patient"""
    factory = get_patient_factory()
    return factory.create_model('patient', **kwargs)

def create_adult_patient(**kwargs) -> Patient:
    """Convenience function to create an adult patient"""
    factory = get_patient_factory()
    return factory.create_adult_patient(**kwargs)

def create_minor_patient(**kwargs) -> Patient:
    """Convenience function to create a minor patient"""
    factory = get_patient_factory()
    return factory.create_minor_patient(**kwargs) 