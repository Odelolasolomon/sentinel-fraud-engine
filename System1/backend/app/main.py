import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.v1.risk import router as risk_router
from .middleware.audit_log import log_requests_middleware
from .core.logger import logger

from .db.session import engine
from .db.base_class import Base
from .models.database import IdentityModel, RiskAssessmentModel

from fastapi import Request
from fastapi.responses import JSONResponse

def create_application() -> FastAPI:
    # Ensure tables exist (Initial Demo)
    Base.metadata.create_all(bind=engine)
    
    app = FastAPI(
        title=settings.APP_NAME,
        description="Enterprise-grade Fraud Detection (SI & ATO)",
        version="2.0.0"
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"FATAL Exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Operational Anomaly: Our engineering team has been notified."}
        )

    # Middleware: Security & Audit
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Custom Audit Logic (Performance Tracking)
    @app.middleware("http")
    async def log_duration(request: Request, call_next):
        return await log_requests_middleware(request, call_next)

    # Health Check (Kubernetes/Load Balancer Liveness)
    @app.get("/health", tags=["System"])
    async def health_check():
        return {"status": "ok", "timestamp": time.time(), "engine": "Production Ready"}

    # Include Routes
    app.include_router(risk_router, prefix="/api/v1", tags=["Analysis"])

    return app

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.DEBUG,
        workers=4 # Multi-core scaling for production
    )
