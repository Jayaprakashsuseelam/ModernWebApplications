from datetime import datetime, date
from typing import Dict, List, Any, Optional
import re
from models.base_model import BaseModel

class Patient(BaseModel):
    """
    Patient Model implementing OOP concepts:
    - Inheritance: Extends BaseModel
    - Encapsulation: Private attributes with validation
    - Polymorphism: Custom implementation of abstract methods
    - Abstraction: Hides complex validation logic
    """
    
    def __init__(self, first_name: str, last_name: str, date_of_birth: str, 
                 gender: str, contact_number: str, **kwargs):
        """Initialize Patient with validation"""
        super().__init__(**kwargs)
        
        # Encapsulation: Private attributes with validation
        self._first_name = first_name
        self._last_name = last_name
        self._date_of_birth = date_of_birth
        self._gender = gender
        self._contact_number = contact_number
        
        # Validate on initialization
        if not self.validate():
            raise ValueError("Invalid patient data")
    
    # Encapsulation: Properties with validation
    @property
    def first_name(self) -> str:
        """Get first name"""
        return self._first_name
    
    @first_name.setter
    def first_name(self, value: str):
        """Set first name with validation"""
        if not self._validate_name(value):
            raise ValueError("Invalid first name")
        self._first_name = value
    
    @property
    def last_name(self) -> str:
        """Get last name"""
        return self._last_name
    
    @last_name.setter
    def last_name(self, value: str):
        """Set last name with validation"""
        if not self._validate_name(value):
            raise ValueError("Invalid last name")
        self._last_name = value
    
    @property
    def date_of_birth(self) -> str:
        """Get date of birth"""
        return self._date_of_birth
    
    @date_of_birth.setter
    def date_of_birth(self, value: str):
        """Set date of birth with validation"""
        if not self._validate_date(value):
            raise ValueError("Invalid date of birth")
        self._date_of_birth = value
    
    @property
    def gender(self) -> str:
        """Get gender"""
        return self._gender
    
    @gender.setter
    def gender(self, value: str):
        """Set gender with validation"""
        if not self._validate_gender(value):
            raise ValueError("Invalid gender")
        self._gender = value
    
    @property
    def contact_number(self) -> str:
        """Get contact number"""
        return self._contact_number
    
    @contact_number.setter
    def contact_number(self, value: str):
        """Set contact number with validation"""
        if not self._validate_contact(value):
            raise ValueError("Invalid contact number")
        self._contact_number = value
    
    # Polymorphism: Implementation of abstract methods
    def to_dict(self) -> Dict[str, Any]:
        """Convert patient to dictionary"""
        return {
            'id': self._id,
            'first_name': self._first_name,
            'last_name': self._last_name,
            'date_of_birth': self._date_of_birth,
            'gender': self._gender,
            'contact_number': self._contact_number,
            'created_at': str(self._created_at) if self._created_at else None,
            'updated_at': str(self._updated_at) if self._updated_at else None
        }
    
    def validate(self) -> bool:
        """Validate all patient data"""
        return (
            self._validate_name(self._first_name) and
            self._validate_name(self._last_name) and
            self._validate_date(self._date_of_birth) and
            self._validate_gender(self._gender) and
            self._validate_contact(self._contact_number)
        )
    
    def _get_insert_data(self) -> tuple[List[str], List[Any]]:
        """Get fields and values for INSERT"""
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'contact_number']
        values = [self._first_name, self._last_name, self._date_of_birth, 
                 self._gender, self._contact_number]
        return fields, values
    
    def _get_update_data(self) -> tuple[List[str], List[Any]]:
        """Get fields and values for UPDATE"""
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'contact_number']
        values = [self._first_name, self._last_name, self._date_of_birth, 
                 self._gender, self._contact_number]
        return fields, values
    
    @classmethod
    def _create_from_row(cls, row: tuple) -> 'Patient':
        """Create Patient instance from database row"""
        return cls(
            id=row[0],
            first_name=row[1],
            last_name=row[2],
            date_of_birth=str(row[3]) if row[3] else None,
            gender=row[4],
            contact_number=row[5],
            created_at=row[6] if len(row) > 6 else None,
            updated_at=row[7] if len(row) > 7 else None
        )
    
    # Abstraction: Private validation methods
    def _validate_name(self, name: str) -> bool:
        """Validate name format"""
        if not name or not isinstance(name, str):
            return False
        # Allow letters, spaces, hyphens, and apostrophes
        return bool(re.match(r"^[A-Za-z\s\-']{2,50}$", name.strip()))
    
    def _validate_date(self, date_str: str) -> bool:
        """Validate date format"""
        if not date_str or not isinstance(date_str, str):
            return False
        try:
            # Check if it's a valid date in YYYY-MM-DD format
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            # Check if date is not in the future
            return parsed_date <= date.today()
        except ValueError:
            return False
    
    def _validate_gender(self, gender: str) -> bool:
        """Validate gender"""
        if not gender or not isinstance(gender, str):
            return False
        return gender.strip().lower() in ['male', 'female', 'other']
    
    def _validate_contact(self, contact: str) -> bool:
        """Validate contact number"""
        if not contact or not isinstance(contact, str):
            return False
        # Remove all non-digit characters and check length
        digits_only = re.sub(r'\D', '', contact)
        return 7 <= len(digits_only) <= 15
    
    # Business logic methods
    def get_full_name(self) -> str:
        """Get patient's full name"""
        return f"{self._first_name} {self._last_name}"
    
    def get_age(self) -> Optional[int]:
        """Calculate patient's age"""
        try:
            birth_date = datetime.strptime(self._date_of_birth, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - birth_date.year
            if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                age -= 1
            return age
        except (ValueError, TypeError):
            return None
    
    def is_adult(self) -> bool:
        """Check if patient is adult (18+)"""
        age = self.get_age()
        return age is not None and age >= 18
    
    def get_formatted_contact(self) -> str:
        """Get formatted contact number"""
        digits_only = re.sub(r'\D', '', self._contact_number)
        if len(digits_only) == 10:
            return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
        return self._contact_number
    
    # Class methods for advanced queries
    @classmethod
    def search_by_name(cls, name: str) -> List['Patient']:
        """Search patients by name (first or last)"""
        try:
            from db import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            
            search_term = f"%{name.lower()}%"
            cursor.execute("""
                SELECT * FROM patients 
                WHERE LOWER(first_name) LIKE %s OR LOWER(last_name) LIKE %s 
                ORDER BY first_name, last_name
            """, (search_term, search_term))
            
            rows = cursor.fetchall()
            return [cls._create_from_row(row) for row in rows]
            
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()
    
    @classmethod
    def get_by_gender(cls, gender: str) -> List['Patient']:
        """Get patients by gender"""
        try:
            from db import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM patients WHERE LOWER(gender) = %s ORDER BY first_name", 
                         (gender.lower(),))
            
            rows = cursor.fetchall()
            return [cls._create_from_row(row) for row in rows]
            
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()
    
    @classmethod
    def get_adults(cls) -> List['Patient']:
        """Get all adult patients (18+)"""
        try:
            from db import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            
            # Calculate age and filter adults
            cursor.execute("""
                SELECT *, 
                       EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) as age
                FROM patients 
                WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) >= 18
                ORDER BY first_name, last_name
            """)
            
            rows = cursor.fetchall()
            return [cls._create_from_row(row) for row in rows]
            
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()
    
    # Magic methods for better object representation
    def __str__(self) -> str:
        """String representation"""
        return f"Patient({self.get_full_name()}, ID: {self._id})"
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        return f"Patient(id={self._id}, name='{self.get_full_name()}', age={self.get_age()})" 