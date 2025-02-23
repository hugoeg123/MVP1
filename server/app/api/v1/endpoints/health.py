from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from app.db.session import get_db
from app.core.config import settings

router = APIRouter()

@router.get("/live")
async def liveness():
    """Basic liveness probe to check if the application is running."""
    return {"status": "ok"}

@router.get("/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    """Comprehensive readiness probe that checks database and cache connectivity."""
    try:
        # Test PostgreSQL connection
        await db.execute("SELECT 1")
        
        # Test Redis connection
        redis = Redis.from_url(settings.REDIS_URL)
        if not redis.ping():
            raise HTTPException(
                status_code=503,
                detail="Redis connection failed"
            )
        
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unavailable: {str(e)}"
        )