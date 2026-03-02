import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.v1.scan import router as scan_router
from .middleware.audit_log import log_requests_middleware
from .core.logger import logger

from .db.session import engine
from .db.base_class import Base
from .models.database import ProfileModel, SessionLogModel

from fastapi.responses import JSONResponse

def create_application() -> FastAPI:
    # Ensure tables exist (Initial Demo & Production check)
    Base.metadata.create_all(bind=engine)
    
    app = FastAPI(
        title=settings.APP_NAME,
        description="Continuous Authentication & Behavioral Biometrics Engine",
        version="2.0.0"
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"FATAL Exception (Biometrics): {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Critical Backend Analytical Error"}
        )

    # Middleware: Security & Monitoring

    # Middleware: Security & Monitoring 
    app.add_middleware( 
        CORSMiddleware,
        allow_origins=[str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.middleware("http")
    async def log_duration(request: Request, call_next):
        return await log_requests_middleware(request, call_next)

    # Health Check (K8s)
    @app.get("/health", tags=["System"])
    async def health_check():
        return {"status": "ok", "system": "Biometrics Engine 2.0"}

    # Include Routes
    app.include_router(scan_router, prefix="/api/v1", tags=["Biometric Verification"])

    return app

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8001, 
        reload=settings.DEBUG,
        workers=4 # Multi-worker for session biometric processing
    )
