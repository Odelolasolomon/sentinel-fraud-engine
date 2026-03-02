import time
from fastapi import Request
from .logger import logger

async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    # Audit Logging for fraud-relevant endpoints (Assessment metrics)
    logger.info(
        f"Path: {request.url.path} | Method: {request.method} | "
        f"Status: {response.status_code} | Process Time: {process_time:.2f}ms"
    )
    return response
