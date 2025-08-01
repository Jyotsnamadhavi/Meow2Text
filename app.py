"""
Entry point for Meow2Text application.
"""
from src.main import app

if __name__ == "__main__":
    import uvicorn
    from src.core.config import settings
    
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    ) 