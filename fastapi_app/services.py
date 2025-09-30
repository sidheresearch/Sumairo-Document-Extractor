import os
import asyncio
import time
from typing import Type, Dict, Any, Optional
from pydantic import BaseModel
from google import genai
from deep_translator import GoogleTranslator
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentExtractionService:
    """Service for extracting structured data from documents using Google Gemini AI"""
    
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_id = settings.GEMINI_MODEL_ID
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def extract_structured_data(self, file_path: str, model: Type[BaseModel]) -> Optional[BaseModel]:
        """
        Extract structured data from a document file using the specified Pydantic model
        
        Args:
            file_path: Path to the document file
            model: Pydantic model class for structured extraction
            
        Returns:
            Extracted data as Pydantic model instance
        """
        try:
            # Upload the file to the File API
            file_name = os.path.basename(file_path).split('.')[0]
            file = self.client.files.upload(
                file=file_path, 
                config={'display_name': file_name}
            )
            
            logger.info(f"Uploaded file: {file.display_name}")
            
            # Count tokens for logging
            try:
                file_size = self.client.models.count_tokens(
                    model=self.model_id, 
                    contents=file
                )
                logger.info(f"File {file.display_name} equals to {file_size.total_tokens} tokens")
            except Exception as e:
                logger.warning(f"Could not count tokens: {e}")
            
            # Generate structured response using the Gemini API
            prompt = f"Extract the structured data from the following document file"
            
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_id,
                contents=[prompt, file],
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': model
                }
            )
            
            # Convert the response to the pydantic model and return it
            if response.parsed:
                logger.info(f"Successfully extracted data using {model.__name__} model")
                return response.parsed
            else:
                logger.warning("No data extracted from the document")
                return None
                
        except Exception as e:
            error_message = str(e)
            logger.error(f"Error during structured data extraction: {error_message}")
            
            # Check if it's a service overload error
            if "503" in error_message or "overloaded" in error_message.lower():
                raise Exception(f"Google Gemini API is temporarily overloaded. Please try again in a few minutes. Error: {error_message}")
            elif "401" in error_message or "authentication" in error_message.lower():
                raise Exception(f"Authentication failed. Please check your GEMINI_API_KEY in the .env file. Error: {error_message}")
            elif "429" in error_message or "quota" in error_message.lower():
                raise Exception(f"API quota exceeded. Please check your usage limits or try again later. Error: {error_message}")
            else:
                raise Exception(f"Failed to extract structured data: {error_message}")

class TranslationService:
    """Service for text extraction and translation using Google Gemini AI and Google Translate"""
    
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_id = settings.GEMINI_MODEL_ID
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def extract_and_translate_text(self, file_path: str, target_language: str = 'en') -> Dict[str, Any]:
        """
        Extract text from document and translate it
        
        Args:
            file_path: Path to the document file
            target_language: Target language code (default: 'en')
            
        Returns:
            Dictionary containing extracted and translated text with metadata
        """
        try:
            # Upload the file to the File API
            file_name = os.path.basename(file_path).split('.')[0]
            file = self.client.files.upload(
                file=file_path,
                config={'display_name': file_name}
            )
            
            logger.info(f"Uploaded file for translation: {file.display_name}")
            
            # Count tokens
            token_count = 0
            try:
                file_size = self.client.models.count_tokens(
                    model=self.model_id,
                    contents=file
                )
                token_count = file_size.total_tokens
                logger.info(f"File {file.display_name} equals to {token_count} tokens")
            except Exception as e:
                logger.warning(f"Could not count tokens: {e}")
            
            # Extract text from the document
            prompt = "Extract all the text from this document. Return only the text content without any formatting or additional commentary."
            
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_id,
                contents=[prompt, file]
            )
            
            extracted_text = response.text if response.text else ""
            
            if not extracted_text.strip():
                logger.warning("No text extracted from the document")
                return {
                    "extracted_text": "",
                    "translated_text": "",
                    "detected_language": "unknown",
                    "token_count": token_count
                }
            
            logger.info(f"Extracted text length: {len(extracted_text)} characters")
            
            # Translate the extracted text
            translator = GoogleTranslator(source='auto', target=target_language)
            translated_text = await asyncio.to_thread(
                translator.translate,
                extracted_text
            )
            
            # Detect source language
            detected_language = "auto-detected"
            try:
                # Try to detect the language using a separate translator instance
                detector = GoogleTranslator(source='auto', target='en')
                # The GoogleTranslator doesn't directly provide language detection
                # So we'll use a workaround or set it as auto-detected
                detected_language = "auto-detected"
            except Exception as e:
                logger.warning(f"Could not detect language: {e}")
            
            logger.info(f"Successfully translated text to {target_language}")
            
            return {
                "extracted_text": extracted_text,
                "translated_text": translated_text,
                "detected_language": detected_language,
                "token_count": token_count
            }
            
        except Exception as e:
            error_message = str(e)
            logger.error(f"Error during text extraction and translation: {error_message}")
            
            # Check if it's a service overload error
            if "503" in error_message or "overloaded" in error_message.lower():
                raise Exception(f"Google Gemini API is temporarily overloaded. Please try again in a few minutes. Error: {error_message}")
            elif "401" in error_message or "authentication" in error_message.lower():
                raise Exception(f"Authentication failed. Please check your GEMINI_API_KEY in the .env file. Error: {error_message}")
            elif "429" in error_message or "quota" in error_message.lower():
                raise Exception(f"API quota exceeded. Please check your usage limits or try again later. Error: {error_message}")
            else:
                raise Exception(f"Failed to extract and translate text: {error_message}")