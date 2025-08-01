"""
Entry point for Meow2Text application.
"""
from backend.src.main import app

if __name__ == "__main__":
    import uvicorn
    from backend.src.core.config import settings
    
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    ) 