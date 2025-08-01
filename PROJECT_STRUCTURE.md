# Meow2Text Project Structure

This document describes the modular, production-ready structure of the Meow2Text application following open-source best practices.

## 📁 Directory Structure

```
Meow2Text/
├── backend/                      # Backend source code
│   └── src/                      # Main source code
│       ├── __init__.py
│       ├── main.py               # FastAPI application factory
│       ├── api/                  # API layer
│       │   ├── __init__.py
│       │   └── routes.py         # API endpoints
│       ├── core/                 # Core functionality
│       │   ├── __init__.py
│       │   ├── config.py         # Application configuration
│       │   └── exceptions.py     # Custom exceptions
│       ├── models/               # Data models
│       │   ├── __init__.py
│       │   └── schemas.py        # Pydantic schemas
│       └── services/             # Business logic services
│           ├── __init__.py
│           ├── audio_service.py      # Audio processing
│           ├── classification_service.py  # Meow classification
│           └── translation_service.py     # LangChain translation
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── services/             # API services
│   │   └── types.ts              # TypeScript types
│   └── package.json
├── tests/                        # Test suite (to be added)
├── docs/                         # Documentation (to be added)
├── app.py                        # Application entry point
├── pyproject.toml               # Modern Python project config
├── requirements.txt             # Python dependencies
├── quick_start.sh               # Backend startup script
├── start_frontend.sh            # Frontend startup script
├── README.md                    # Main documentation
├── CONTRIBUTING.md              # Contribution guidelines
├── PROJECT_STRUCTURE.md         # This file
├── SETUP.md                     # Setup instructions
└── .gitignore                   # Git ignore rules
```

## 🏗️ Architecture Overview

### **Layered Architecture**

```
┌─────────────────────────────────────┐
│           Frontend (React)          │
├─────────────────────────────────────┤
│           API Layer (FastAPI)       │
├─────────────────────────────────────┤
│         Service Layer               │
│  ┌─────────┬─────────┬─────────┐   │
│  │ Audio   │Classify │Translate│   │
│  │Service  │Service  │Service  │   │
│  └─────────┴─────────┴─────────┘   │
├─────────────────────────────────────┤
│         Core Layer                  │
│  ┌─────────┬─────────┬─────────┐   │
│  │ Config  │Exceptions│ Models │   │
│  └─────────┴─────────┴─────────┘   │
└─────────────────────────────────────┘
```

## 📦 Module Descriptions

### **API Layer (`backend/src/api/`)**
- **Purpose**: HTTP request/response handling
- **Components**: FastAPI routes, request validation, response formatting
- **Key Files**: `routes.py` - All API endpoints

### **Core Layer (`backend/src/core/`)**
- **Purpose**: Application foundation and configuration
- **Components**: 
  - `config.py` - Centralized configuration using Pydantic Settings
  - `exceptions.py` - Custom exception hierarchy
- **Benefits**: Centralized configuration, proper error handling

### **Models Layer (`backend/src/models/`)**
- **Purpose**: Data validation and serialization
- **Components**: Pydantic schemas for API requests/responses
- **Benefits**: Type safety, automatic validation, OpenAPI documentation

### **Services Layer (`backend/src/services/`)**
- **Purpose**: Business logic implementation
- **Components**:
  - `audio_service.py` - Audio processing and validation
  - `classification_service.py` - Meow classification logic
  - `translation_service.py` - LangChain translation logic
- **Benefits**: Separation of concerns, testability, reusability

## 🔧 Key Features

### **1. Configuration Management**
```python
# backend/src/core/config.py
class Settings(BaseSettings):
    app_name: str = "Meow2Text API"
    openai_api_key: str = ""
    # ... other settings
    
    class Config:
        env_file = ".env"
```

### **2. Service Pattern**
```python
# backend/src/services/audio_service.py
class AudioService:
    def preprocess_audio(self, audio_path: str) -> np.ndarray:
        # Business logic here
        pass

# Global instance
audio_service = AudioService()
```

### **3. Custom Exceptions**
```python
# backend/src/core/exceptions.py
class Meow2TextError(Exception):
    """Base exception for Meow2Text application."""
    pass

class AudioProcessingError(Meow2TextError):
    """Raised when audio processing fails."""
    pass
```

### **4. Pydantic Schemas**
```python
# backend/src/models/schemas.py
class ClassificationResult(BaseModel):
    category: str = Field(..., description="Meow category")
    confidence: float = Field(..., ge=0.0, le=1.0)
    # ... other fields
```

## 🚀 Benefits of This Structure

### **1. Maintainability**
- Clear separation of concerns
- Modular design allows easy updates
- Consistent code organization

### **2. Testability**
- Services can be unit tested independently
- Mock dependencies easily
- Clear interfaces between layers

### **3. Scalability**
- Easy to add new services
- Simple to extend API endpoints
- Configuration-driven behavior

### **4. Developer Experience**
- Clear project structure
- Type hints throughout
- Comprehensive documentation
- Modern Python tooling

### **5. Production Ready**
- Proper error handling
- Configuration management
- API documentation
- Logging support (ready to add)

## 🔄 Development Workflow

### **Adding New Features**
1. **New Service**: Add to `backend/src/services/`
2. **New API**: Add to `backend/src/api/routes.py`
3. **New Models**: Add to `backend/src/models/schemas.py`
4. **Configuration**: Add to `backend/src/core/config.py`

### **Testing**
```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=backend

# Run specific service tests
pytest tests/test_audio_service.py
```

### **Code Quality**
```bash
# Format code
black backend/
isort backend/

# Type checking
mypy backend/

# Linting
flake8 backend/
```

## 📈 Future Enhancements

### **Planned Additions**
- **Tests**: Comprehensive test suite
- **Logging**: Structured logging with loguru
- **Monitoring**: Health checks and metrics
- **Caching**: Redis integration for performance
- **Database**: PostgreSQL for user data
- **Authentication**: JWT-based auth system
- **Deployment**: Docker and CI/CD pipelines

### **Extensibility Points**
- **New Audio Formats**: Extend `AudioService`
- **New Personalities**: Extend `TranslationService`
- **New Classification Models**: Extend `ClassificationService`
- **New API Endpoints**: Add to `routes.py`

## 🎯 Best Practices Followed

1. **SOLID Principles**: Single responsibility, dependency injection
2. **Clean Architecture**: Clear layer separation
3. **Type Safety**: Type hints throughout
4. **Error Handling**: Custom exception hierarchy
5. **Configuration**: Environment-based configuration
6. **Documentation**: Comprehensive docstrings
7. **Testing**: Ready for comprehensive testing
8. **Modern Python**: Using latest Python features and tools

This structure provides a solid foundation for a production-ready, maintainable, and scalable application while following open-source best practices. 