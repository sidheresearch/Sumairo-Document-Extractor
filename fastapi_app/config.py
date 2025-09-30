import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # API Configuration
    API_TITLE: str = "Document Extractor API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API for extracting structured data from documents using Google Gemini AI"
    
    # Google Gemini AI Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL_ID: str = os.getenv("GEMINI_MODEL_ID", "gemini-2.0-flash")
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB in bytes
    ALLOWED_FILE_EXTENSIONS: set = {".pdf", ".jpg", ".jpeg", ".png"}
    
    # Translation Configuration
    DEFAULT_TARGET_LANGUAGE: str = "en"
    
    # CORS Configuration
    CORS_ORIGINS: list = ["*"]  # Configure properly in production
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# Create settings instance
settings = Settings()

def validate_settings():
    """Validate required settings"""
    errors = []
    
    if not settings.GEMINI_API_KEY:
        errors.append("GEMINI_API_KEY environment variable is required")
    
    if errors:
        raise ValueError("Configuration errors: " + "; ".join(errors))

# Validate settings on import
validate_settings()