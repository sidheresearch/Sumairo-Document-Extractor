from fastapi import FastAPI, File, UploadFile, HTTPException, Form as FormField
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import tempfile
import os
import logging
from enum import Enum

from models import *
from services import DocumentExtractionService, TranslationService
from config import settings
from utils import (
    validate_file_size, 
    validate_file_type, 
    format_extraction_response,
    format_translation_response,
    log_request_info,
    handle_service_error
)

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Initialize services
extraction_service = DocumentExtractionService()
translation_service = TranslationService()

class DocumentType(str, Enum):
    INVOICE = "Invoice"
    FORM = "Form"
    BUSINESS_CARD = "BusinessCard"
    TENDER_DOCUMENT = "TenderDocument"
    PERSON = "Person"
    TRANSLATE_TEXT = "TranslateText"

@app.get("/")
async def root():
    """Root endpoint providing API information"""
    return {
        "message": "Document Extractor API",
        "version": "1.0.0",
        "endpoints": {
            "/extract": "Extract structured data from documents",
            "/translate": "Extract and translate text from documents",
            "/health": "Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Document Extractor API"}

@app.post("/extract")
async def extract_document_data(
    file: UploadFile = File(...),
    document_type: DocumentType = FormField(...)
):
    """
    Extract structured data from uploaded document
    
    - **file**: Document file (PDF, JPG, JPEG, PNG)
    - **document_type**: Type of document to extract data for
    """
    
    try:
        # Read file content
        content = await file.read()
        
        # Validate file size and type
        validate_file_size(content)
        file_extension = validate_file_type(file.filename, content)
        
        # Log request info
        log_request_info(file.filename, document_type.value, "extraction")
        
        # Handle translation request
        if document_type == DocumentType.TRANSLATE_TEXT:
            return await translate_document_text_internal(file.filename, content, file_extension)
        
        # Map document type to Pydantic model
        model_mapping = {
            DocumentType.INVOICE: Invoice,
            DocumentType.FORM: Form,
            DocumentType.BUSINESS_CARD: BusinessCard,
            DocumentType.TENDER_DOCUMENT: TenderDocument,
            DocumentType.PERSON: Person
        }
        
        selected_model = model_mapping.get(document_type)
        if not selected_model:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid document type: {document_type}"
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Extract structured data
            extracted_data = await extraction_service.extract_structured_data(
                temp_file_path, 
                selected_model
            )
            
            return format_extraction_response(
                success=True,
                document_type=document_type.value,
                filename=file.filename,
                data=extracted_data
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during extraction: {str(e)}")
        raise handle_service_error(e, "extraction")

async def translate_document_text_internal(filename: str, content: bytes, file_extension: str):
    """Internal function to handle text translation"""
    try:
        log_request_info(filename, "TranslateText", "translation")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Extract and translate text
            result = await translation_service.extract_and_translate_text(temp_file_path)
            
            return format_translation_response(
                success=True,
                filename=filename,
                extracted_text=result.get("extracted_text"),
                translated_text=result.get("translated_text"),
                detected_language=result.get("detected_language"),
                token_count=result.get("token_count")
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise handle_service_error(e, "translation")

@app.post("/translate")
async def translate_document_text(file: UploadFile = File(...)):
    """
    Extract and translate text from uploaded document
    
    - **file**: Document file (PDF, JPG, JPEG, PNG)
    """
    
    try:
        # Read file content
        content = await file.read()
        
        # Validate file size and type
        validate_file_size(content)
        file_extension = validate_file_type(file.filename, content)
        
        # Use internal translation function
        return await translate_document_text_internal(file.filename, content, file_extension)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during translation: {str(e)}")
        raise handle_service_error(e, "translation")

@app.get("/supported-types")
async def get_supported_document_types():
    """Get list of supported document types"""
    return {
        "supported_types": [
            {
                "type": "Invoice",
                "description": "Extract invoice number, date, items, and total gross worth"
            },
            {
                "type": "Form", 
                "description": "Extract form number, dates, and plan liabilities"
            },
            {
                "type": "BusinessCard",
                "description": "Extract contact information from business cards"
            },
            {
                "type": "TenderDocument", 
                "description": "Extract comprehensive tender document information"
            },
            {
                "type": "Person",
                "description": "Extract person information including name, age, and work topics"
            },
            {
                "type": "TranslateText",
                "description": "Extract and translate text from documents"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)