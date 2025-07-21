from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from database import get_db
from models import Employee, User
from auth import get_current_active_user

router = APIRouter(prefix="/employees", tags=["employees"])

# Pydantic models for request/response
class EmployeeBase(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    department: str
    position: str
    hire_date: datetime
    salary: Optional[int] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    employee_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    hire_date: Optional[datetime] = None
    salary: Optional[int] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    is_active: Optional[bool] = None

class EmployeeResponse(EmployeeBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=EmployeeResponse)
def create_employee(
    employee: EmployeeCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    # Check if employee_id already exists
    db_employee = db.query(Employee).filter(Employee.employee_id == employee.employee_id).first()
    if db_employee:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    
    # Check if email already exists
    db_employee = db.query(Employee).filter(Employee.email == employee.email).first()
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    
    return db_employee

@router.get("/", response_model=List[EmployeeResponse])
def get_employees(
    skip: int = 0, 
    limit: int = 100, 
    department: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Employee)
    
    if department:
        query = query.filter(Employee.department == department)
    
    if is_active is not None:
        query = query.filter(Employee.is_active == is_active)
    
    employees = query.offset(skip).limit(limit).all()
    return employees

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: str, 
    employee_update: EmployeeUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check if new email conflicts with existing employee
    if employee_update.email and employee_update.email != db_employee.email:
        existing_employee = db.query(Employee).filter(Employee.email == employee_update.email).first()
        if existing_employee:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update employee fields
    update_data = employee_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_employee, field, value)
    
    db.commit()
    db.refresh(db_employee)
    
    return db_employee

@router.delete("/{employee_id}")
def delete_employee(
    employee_id: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    
    return {"message": "Employee deleted successfully"}

@router.patch("/{employee_id}/deactivate")
def deactivate_employee(
    employee_id: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db_employee.is_active = False
    db.commit()
    
    return {"message": "Employee deactivated successfully"}

@router.patch("/{employee_id}/activate")
def activate_employee(
    employee_id: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db_employee.is_active = True
    db.commit()
    
    return {"message": "Employee activated successfully"} 