from fastapi import HTTPException
from typing import List, Dict, Any
import os
import magic
import logging

from config import settings

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom validation error"""
    pass

def validate_file_size(file_content: bytes) -> None:
    """Validate uploaded file size"""
    file_size = len(file_content)
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size allowed: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
        )

def validate_file_type(filename: str, file_content: bytes) -> str:
    """
    Validate file type using both extension and magic number
    Returns the validated file extension
    """
    # Check file extension
    file_extension = os.path.splitext(filename)[1].lower()
    if file_extension not in settings.ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file_extension}'. Allowed types: {', '.join(settings.ALLOWED_FILE_EXTENSIONS)}"
        )
    
    # Additional validation using python-magic if available
    try:
        import magic
        file_type = magic.from_buffer(file_content, mime=True)
        
        # Map MIME types to extensions for validation
        mime_to_ext = {
            'application/pdf': '.pdf',
            'image/jpeg': '.jpg',
            'image/jpg': '.jpg', 
            'image/png': '.png'
        }
        
        expected_ext = mime_to_ext.get(file_type)
        if expected_ext and expected_ext != file_extension:
            if not (expected_ext == '.jpg' and file_extension == '.jpeg'):  # Allow jpeg/jpg variation
                logger.warning(f"File extension {file_extension} doesn't match MIME type {file_type}")
                
    except ImportError:
        # python-magic not installed, skip MIME type validation
        logger.info("python-magic not available, skipping MIME type validation")
    except Exception as e:
        logger.warning(f"Could not validate MIME type: {e}")
    
    return file_extension

def format_extraction_response(
    success: bool,
    document_type: str,
    filename: str,
    data: Any = None,
    error: str = None,
    formatted_output: str = None
) -> Dict[str, Any]:
    """Format extraction API response"""
    response = {
        "success": success,
        "document_type": document_type,
        "filename": filename
    }
    if success and data:
        response["data"] = data.model_dump() if hasattr(data, 'model_dump') else data
    if success and formatted_output:
        response["formatted_output"] = formatted_output
    elif not success and error:
        response["error"] = error
    return response

def format_translation_response(
    success: bool,
    filename: str,
    extracted_text: str = None,
    translated_text: str = None,
    detected_language: str = None,
    token_count: int = None,
    error: str = None
) -> Dict[str, Any]:
    """Format translation API response"""
    response = {
        "success": success,
        "filename": filename
    }
    
    if success:
        response.update({
            "extracted_text": extracted_text,
            "translated_text": translated_text,
            "detected_language": detected_language,
            "token_count": token_count
        })
    elif error:
        response["error"] = error
    
    return response

def log_request_info(filename: str, document_type: str = None, operation: str = "extraction"):
    """Log request information"""
    logger.info(f"Processing {operation} request - File: {filename}, Type: {document_type}")

def handle_service_error(e: Exception, operation: str = "processing") -> HTTPException:
    """Convert service errors to appropriate HTTP exceptions"""
    error_message = str(e)
    logger.error(f"Service error during {operation}: {error_message}")
    
    # Map specific errors to appropriate status codes
    if "authentication" in error_message.lower() or "api key" in error_message.lower():
        return HTTPException(
            status_code=401,
            detail="Authentication failed. Please check API key configuration."
        )
    elif "quota" in error_message.lower() or "rate limit" in error_message.lower():
        return HTTPException(
            status_code=429,
            detail="API quota exceeded or rate limit reached. Please try again later."
        )
    elif "timeout" in error_message.lower():
        return HTTPException(
            status_code=504,
            detail="Request timeout. Please try again with a smaller file."
        )
    else:
        return HTTPException(
            status_code=500,
            detail=f"Internal server error during {operation}: {error_message}"
        )