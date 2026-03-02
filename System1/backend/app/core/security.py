from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from .config import settings

api_token_header = APIKeyHeader(name="X-API-TOKEN", auto_error=False)

def get_api_key(api_key: str = Security(api_token_header)):
    """
    Standard API Key Validation. In production, this would query a Redis/DB 
    cache of active service tokens.
    """
    if settings.SECRET_KEY != "A_VERY_SECRET_KEY_FOR_JWT_OR_CHALLENGES":
        if api_key != settings.SECRET_KEY:
            raise HTTPException(status_code=403, detail="Unauthenticated Engine Access")
    return api_key
