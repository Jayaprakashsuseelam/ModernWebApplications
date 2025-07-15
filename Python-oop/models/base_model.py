from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
from db import get_connection

class BaseModel(ABC):
    """
    Abstract Base Class implementing core OOP concepts:
    - Abstraction: Abstract methods that must be implemented by subclasses
    - Encapsulation: Private attributes and methods
    - Inheritance: Base class for all models
    - Polymorphism: Different implementations for different model types
    """
    
    def __init__(self, **kwargs):
        """Initialize base model with common attributes"""
        self._id = kwargs.get('id')
        self._created_at = kwargs.get('created_at', datetime.now())
        self._updated_at = kwargs.get('updated_at', datetime.now())
        self._table_name = self.__class__.__name__.lower() + 's'
    
    # Encapsulation: Private attributes with getters/setters
    @property
    def id(self) -> Optional[int]:
        """Get the model ID"""
        return self._id
    
    @id.setter
    def id(self, value: int):
        """Set the model ID"""
        self._id = value
    
    @property
    def created_at(self) -> datetime:
        """Get creation timestamp"""
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        """Get last update timestamp"""
        return self._updated_at
    
    @updated_at.setter
    def updated_at(self, value: datetime):
        """Set last update timestamp"""
        self._updated_at = value
    
    # Abstraction: Abstract methods that must be implemented
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate model data - must be implemented by subclasses"""
        pass
    
    # Polymorphism: Common methods with different implementations
    def save(self) -> bool:
        """Save model to database"""
        if not self.validate():
            raise ValueError("Model validation failed")
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if self._id is None:
                # Insert new record
                fields, values = self._get_insert_data()
                placeholders = ', '.join(['%s'] * len(fields))
                query = f"INSERT INTO {self._table_name} ({', '.join(fields)}) VALUES ({placeholders}) RETURNING id, created_at, updated_at"
                
                cursor.execute(query, values)
                result = cursor.fetchone()
                self._id = result[0]
                self._created_at = result[1]
                self._updated_at = result[2]
            else:
                # Update existing record
                fields, values = self._get_update_data()
                if fields:
                    set_clause = ', '.join([f"{field} = %s" for field in fields])
                    values.append(self._id)
                    query = f"UPDATE {self._table_name} SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING updated_at"
                    
                    cursor.execute(query, values)
                    result = cursor.fetchone()
                    self._updated_at = result[0]
            
            conn.commit()
            return True
            
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def delete(self) -> bool:
        """Delete model from database"""
        if self._id is None:
            return False
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute(f"DELETE FROM {self._table_name} WHERE id = %s", (self._id,))
            deleted = cursor.rowcount > 0
            conn.commit()
            
            if deleted:
                self._id = None
            
            return deleted
            
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    # Class methods for database operations
    @classmethod
    def get_by_id(cls, model_id: int) -> Optional['BaseModel']:
        """Get model by ID"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            table_name = cls.__name__.lower() + 's'
            cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (model_id,))
            row = cursor.fetchone()
            
            if row:
                return cls._create_from_row(row)
            return None
            
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()
    
    @classmethod
    def get_all(cls) -> List['BaseModel']:
        """Get all models"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            table_name = cls.__name__.lower() + 's'
            cursor.execute(f"SELECT * FROM {table_name} ORDER BY id")
            rows = cursor.fetchall()
            
            return [cls._create_from_row(row) for row in rows]
            
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()
    
    @classmethod
    def count(cls) -> int:
        """Count total number of models"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            table_name = cls.__name__.lower() + 's'
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return cursor.fetchone()[0]
            
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()
    
    # Abstract methods that must be implemented by subclasses
    @abstractmethod
    def _get_insert_data(self) -> tuple[List[str], List[Any]]:
        """Get fields and values for INSERT - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def _get_update_data(self) -> tuple[List[str], List[Any]]:
        """Get fields and values for UPDATE - must be implemented by subclasses"""
        pass
    
    @classmethod
    @abstractmethod
    def _create_from_row(cls, row: tuple) -> 'BaseModel':
        """Create model instance from database row - must be implemented by subclasses"""
        pass
    
    # Magic methods for better object representation
    def __str__(self) -> str:
        """String representation of the model"""
        return f"{self.__class__.__name__}(id={self._id})"
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        return f"{self.__class__.__name__}(id={self._id}, created_at={self._created_at})"
    
    def __eq__(self, other) -> bool:
        """Compare models by ID"""
        if not isinstance(other, self.__class__):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        """Hash based on ID"""
        return hash(self._id)
    
    # JSON serialization
    def to_json(self) -> str:
        """Convert model to JSON string"""
        return json.dumps(self.to_dict(), default=str)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'BaseModel':
        """Create model from JSON string"""
        data = json.loads(json_str)
        return cls(**data) 