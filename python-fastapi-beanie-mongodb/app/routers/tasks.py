from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskList
from app.services.task_service import TaskService
from app.core.deps import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.models.task import TaskStatus, TaskPriority

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new task"""
    task = await TaskService.create_task(task_data, str(current_user.id))
    return TaskResponse(
        id=str(task.id),
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        assigned_to=task.assigned_to,
        created_by=task.created_by,
        due_date=task.due_date,
        completed_at=task.completed_at,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.get("/", response_model=TaskList)
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[TaskStatus] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    current_user: User = Depends(get_current_active_user)
):
    """Get tasks for current user or all tasks for admin"""
    if current_user.role == "admin":
        tasks = await TaskService.get_all_tasks(skip=skip, limit=limit, status=status, priority=priority)
    else:
        tasks = await TaskService.get_tasks_by_user(str(current_user.id), skip=skip, limit=limit, status=status)
    
    total = len(tasks)  # In a real app, you'd want to get total count separately
    
    return TaskList(
        tasks=[
            TaskResponse(
                id=str(task.id),
                title=task.title,
                description=task.description,
                status=task.status,
                priority=task.priority,
                assigned_to=task.assigned_to,
                created_by=task.created_by,
                due_date=task.due_date,
                completed_at=task.completed_at,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ],
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get task by ID"""
    task = await TaskService.get_task_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Check permissions: users can only access their own tasks or assigned tasks
    if (current_user.role != "admin" and 
        str(current_user.id) != task.created_by and 
        str(current_user.id) != task.assigned_to):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return TaskResponse(
        id=str(task.id),
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        assigned_to=task.assigned_to,
        created_by=task.created_by,
        due_date=task.due_date,
        completed_at=task.completed_at,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update task"""
    task = await TaskService.get_task_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Check permissions: users can only update their own tasks or assigned tasks
    if (current_user.role != "admin" and 
        str(current_user.id) != task.created_by and 
        str(current_user.id) != task.assigned_to):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    updated_task = await TaskService.update_task(task_id, task_data)
    return TaskResponse(
        id=str(updated_task.id),
        title=updated_task.title,
        description=updated_task.description,
        status=updated_task.status,
        priority=updated_task.priority,
        assigned_to=updated_task.assigned_to,
        created_by=updated_task.created_by,
        due_date=updated_task.due_date,
        completed_at=updated_task.completed_at,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete task"""
    task = await TaskService.get_task_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Check permissions: only task creator or admin can delete
    if current_user.role != "admin" and str(current_user.id) != task.created_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    success = await TaskService.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )
    
    return {"message": "Task deleted successfully"}


@router.put("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Mark task as completed"""
    task = await TaskService.get_task_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Check permissions: users can only complete their own tasks or assigned tasks
    if (current_user.role != "admin" and 
        str(current_user.id) != task.created_by and 
        str(current_user.id) != task.assigned_to):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    completed_task = await TaskService.mark_task_completed(task_id)
    return TaskResponse(
        id=str(completed_task.id),
        title=completed_task.title,
        description=completed_task.description,
        status=completed_task.status,
        priority=completed_task.priority,
        assigned_to=completed_task.assigned_to,
        created_by=completed_task.created_by,
        due_date=completed_task.due_date,
        completed_at=completed_task.completed_at,
        created_at=completed_task.created_at,
        updated_at=completed_task.updated_at
    )


@router.put("/{task_id}/assign/{user_id}")
async def assign_task(
    task_id: str,
    user_id: str,
    current_user: User = Depends(get_current_admin_user)
):
    """Assign task to a user (admin only)"""
    task = await TaskService.assign_task(task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task or user not found"
        )
    
    return {"message": f"Task assigned to user {user_id}"}


@router.get("/statistics/me")
async def get_my_task_statistics(
    current_user: User = Depends(get_current_active_user)
):
    """Get task statistics for current user"""
    stats = await TaskService.get_task_statistics(str(current_user.id))
    return stats 