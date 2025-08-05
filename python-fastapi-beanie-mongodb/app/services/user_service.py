from typing import Optional, List
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.core.security import create_access_token
from datetime import timedelta
from app.core.config import settings


class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = await User.find_one(
            (User.email == user_data.email) | (User.username == user_data.username)
        )
        if existing_user:
            raise ValueError("User with this email or username already exists")
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password
        )
        return await user.insert()
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """Get user by ID"""
        return await User.get(user_id)
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        return await User.find_one(User.email == email)
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """Get user by username"""
        return await User.find_one(User.username == username)
    
    @staticmethod
    async def get_all_users(skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return await User.find_all().skip(skip).limit(limit).to_list()
    
    @staticmethod
    async def update_user(user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Update user"""
        user = await User.get(user_id)
        if not user:
            return None
        
        update_data = user_data.dict(exclude_unset=True)
        
        # Hash password if provided
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # Update user
        await user.update({"$set": update_data})
        await user.update_timestamp()
        return user
    
    @staticmethod
    async def delete_user(user_id: str) -> bool:
        """Delete user"""
        user = await User.get(user_id)
        if not user:
            return False
        
        await user.delete()
        return True
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = await User.find_one(User.email == email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def create_user_token(user: User) -> str:
        """Create access token for user"""
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        return create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
    
    @staticmethod
    async def change_user_role(user_id: str, new_role: UserRole) -> Optional[User]:
        """Change user role (admin only)"""
        user = await User.get(user_id)
        if not user:
            return None
        
        user.role = new_role
        await user.update_timestamp()
        return user 