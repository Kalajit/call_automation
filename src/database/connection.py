import asyncpg
from typing import Optional
from src.config.settings import (
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
)
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

# Global database pool
db_pool: Optional[asyncpg.Pool] = None


async def init_db():
    """Initialize database connection pool"""
    global db_pool
    db_pool = await asyncpg.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        min_size=5,
        max_size=20,
        command_timeout=60
    )
    logger.info("✅ Database pool initialized")


async def close_db():
    """Close database connection pool"""
    global db_pool
    if db_pool:
        await db_pool.close()
        logger.info("🔴 Database pool closed")


def get_db_pool() -> Optional[asyncpg.Pool]:
    """Get the database pool instance"""
    return db_pool