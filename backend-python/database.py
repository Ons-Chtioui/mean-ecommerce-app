import logging
import sys
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import settings

logger = logging.getLogger(__name__)

_client: AsyncIOMotorClient = None
_db: AsyncIOMotorDatabase = None


async def connect_to_mongo():
    """Connect to MongoDB on application startup."""
    global _client, _db
    try:
        _client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
        # Verify connection
        await _client.admin.command("ping")
        _db = _client[settings.DATABASE_NAME]
        # Create indexes
        await _db["categories"].create_index("name", unique=True)
        await _db["products"].create_index("category")
        logger.info(f"Connected to MongoDB at {settings.MONGODB_URL}, database: {settings.DATABASE_NAME}")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        sys.exit(1)


async def close_mongo_connection():
    """Close MongoDB connection on application shutdown."""
    global _client
    if _client:
        _client.close()
        logger.info("MongoDB connection closed.")


def get_database() -> AsyncIOMotorDatabase:
    """FastAPI dependency that returns the database instance."""
    return _db
