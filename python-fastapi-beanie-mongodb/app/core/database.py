from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.user import User
from app.models.task import Task


async def init_db():
    """Initialize database connection and Beanie ODM"""
    # Create motor client
    client = AsyncIOMotorClient(settings.mongodb_url)
    
    # Initialize Beanie with the Product (Document) class
    await init_beanie(
        database=client[settings.database_name],
        document_models=[User, Task]
    )


async def close_db():
    """Close database connection"""
    # Motor client will be closed automatically when the application shuts down
    pass 