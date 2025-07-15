from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, TypeVar, Generic
from models.base_model import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseService(ABC, Generic[T]):
    """
    Abstract Base Service implementing OOP concepts:
    - Abstraction: Abstract methods for business logic
    - Generics: Type-safe service operations
    - Composition: Service layer pattern
    - Dependency Inversion: Depends on abstractions, not concretions
    """
    
    def __init__(self, model_class: type[T]):
        """Initialize service with model class"""
        self._model_class = model_class
    
    # CRUD Operations
    def create(self, **kwargs) -> T:
        """Create a new model instance"""
        try:
            instance = self._model_class(**kwargs)
            instance.save()
            return instance
        except Exception as e:
            raise self._handle_error("create", e)
    
    def get_by_id(self, model_id: int) -> Optional[T]:
        """Get model by ID"""
        try:
            return self._model_class.get_by_id(model_id)
        except Exception as e:
            raise self._handle_error("get_by_id", e)
    
    def get_all(self) -> List[T]:
        """Get all models"""
        try:
            return self._model_class.get_all()
        except Exception as e:
            raise self._handle_error("get_all", e)
    
    def update(self, model_id: int, **kwargs) -> Optional[T]:
        """Update model by ID"""
        try:
            instance = self._model_class.get_by_id(model_id)
            if not instance:
                return None
            
            # Update attributes
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            instance.save()
            return instance
        except Exception as e:
            raise self._handle_error("update", e)
    
    def delete(self, model_id: int) -> bool:
        """Delete model by ID"""
        try:
            instance = self._model_class.get_by_id(model_id)
            if not instance:
                return False
            return instance.delete()
        except Exception as e:
            raise self._handle_error("delete", e)
    
    def count(self) -> int:
        """Count total models"""
        try:
            return self._model_class.count()
        except Exception as e:
            raise self._handle_error("count", e)
    
    # Business Logic Methods
    def exists(self, model_id: int) -> bool:
        """Check if model exists"""
        return self.get_by_id(model_id) is not None
    
    def bulk_create(self, data_list: List[Dict[str, Any]]) -> List[T]:
        """Create multiple models"""
        instances = []
        for data in data_list:
            try:
                instance = self.create(**data)
                instances.append(instance)
            except Exception as e:
                # Log error but continue with other items
                print(f"Error creating item: {e}")
        return instances
    
    def bulk_delete(self, model_ids: List[int]) -> int:
        """Delete multiple models"""
        deleted_count = 0
        for model_id in model_ids:
            if self.delete(model_id):
                deleted_count += 1
        return deleted_count
    
    # Abstract methods for subclasses to implement
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate data before creating/updating"""
        pass
    
    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """Get service-specific statistics"""
        pass
    
    # Error handling
    def _handle_error(self, operation: str, error: Exception) -> Exception:
        """Handle and format errors"""
        error_message = f"Error in {self.__class__.__name__}.{operation}: {str(error)}"
        return Exception(error_message)
    
    # Magic methods
    def __len__(self) -> int:
        """Return total count of models"""
        return self.count()
    
    def __contains__(self, model_id: int) -> bool:
        """Check if model exists"""
        return self.exists(model_id) 