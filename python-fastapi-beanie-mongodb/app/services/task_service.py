from typing import Optional, List
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.user import User


class TaskService:
    @staticmethod
    async def create_task(task_data: TaskCreate, created_by: str) -> Task:
        """Create a new task"""
        task = Task(
            **task_data.dict(),
            created_by=created_by
        )
        return await task.insert()
    
    @staticmethod
    async def get_task_by_id(task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return await Task.get(task_id)
    
    @staticmethod
    async def get_tasks_by_user(
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatus] = None
    ) -> List[Task]:
        """Get tasks created by or assigned to a user"""
        query = Task.find(
            (Task.created_by == user_id) | (Task.assigned_to == user_id)
        )
        
        if status:
            query = query.find(Task.status == status)
        
        return await query.skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def get_all_tasks(
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None
    ) -> List[Task]:
        """Get all tasks with optional filters"""
        query = Task.find_all()
        
        if status:
            query = query.find(Task.status == status)
        
        if priority:
            query = query.find(Task.priority == priority)
        
        return await query.skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def update_task(task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """Update task"""
        task = await Task.get(task_id)
        if not task:
            return None
        
        update_data = task_data.dict(exclude_unset=True)
        
        # Update task
        await task.update({"$set": update_data})
        await task.update_timestamp()
        return task
    
    @staticmethod
    async def delete_task(task_id: str) -> bool:
        """Delete task"""
        task = await Task.get(task_id)
        if not task:
            return False
        
        await task.delete()
        return True
    
    @staticmethod
    async def mark_task_completed(task_id: str) -> Optional[Task]:
        """Mark task as completed"""
        task = await Task.get(task_id)
        if not task:
            return None
        
        await task.mark_completed()
        return task
    
    @staticmethod
    async def assign_task(task_id: str, user_id: str) -> Optional[Task]:
        """Assign task to a user"""
        task = await Task.get(task_id)
        if not task:
            return None
        
        # Verify user exists
        user = await User.get(user_id)
        if not user:
            return None
        
        task.assigned_to = user_id
        await task.update_timestamp()
        return task
    
    @staticmethod
    async def get_task_statistics(user_id: str) -> dict:
        """Get task statistics for a user"""
        total_tasks = await Task.find(
            (Task.created_by == user_id) | (Task.assigned_to == user_id)
        ).count()
        
        completed_tasks = await Task.find(
            ((Task.created_by == user_id) | (Task.assigned_to == user_id)) &
            (Task.status == TaskStatus.COMPLETED)
        ).count()
        
        pending_tasks = await Task.find(
            ((Task.created_by == user_id) | (Task.assigned_to == user_id)) &
            (Task.status == TaskStatus.PENDING)
        ).count()
        
        in_progress_tasks = await Task.find(
            ((Task.created_by == user_id) | (Task.assigned_to == user_id)) &
            (Task.status == TaskStatus.IN_PROGRESS)
        ).count()
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        } 