import logging
from fastapi import Request
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("health-mvp")

async def log_middleware(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    duration = (datetime.now() - start_time).total_seconds()
    
    log_data = {
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration": duration
    }
    
    logger.info(f"Request: {log_data}")
    return response