# Document Extractor FastAPI

A powerful FastAPI service that extracts structured data from documents (PDF, images) using Google Gemini AI, with built-in OCR and translation capabilities.

## Features

- **Document Data Extraction**: Extract structured information from various document types:
  - Invoices (invoice number, dates, items, totals)
  - Forms (form numbers, dates, plan liabilities)  
  - Business Cards (contact information)
  - Tender Documents (comprehensive tender information)
  - Person Information (names, ages, work topics)

- **OCR & Translation**: Extract text from documents and translate to English
- **Multi-format Support**: PDF, JPG, JPEG, PNG files
- **RESTful API**: Easy integration with frontend applications
- **Comprehensive Error Handling**: Detailed error messages and validation
- **CORS Support**: Ready for frontend integration

## Project Structure

```
fastapi_app/
├── main.py              # FastAPI application and endpoints
├── models.py            # Pydantic models for structured data
├── services.py          # Core extraction and translation services
├── config.py            # Configuration and settings
├── utils.py             # Utility functions and validation
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This documentation
```

## Prerequisites

- Python 3.8+
- Google Gemini API key ([Get your API key](https://ai.google.dev/))

## Installation

1. **Clone or download the project:**
   ```bash
   cd "Document Extractor/fastapi_app"
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   copy .env.example .env  # On Windows
   # cp .env.example .env  # On macOS/Linux
   ```
   
   Edit `.env` file and add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   GEMINI_MODEL_ID=gemini-2.0-flash
   LOG_LEVEL=INFO
   ```

## Running the Application

1. **Start the server:**
   ```bash
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Access the API:**
   - API Base URL: `http://localhost:8000`
   - Interactive API Documentation: `http://localhost:8000/docs`
   - Alternative API Docs: `http://localhost:8000/redoc`

## API Endpoints

### 1. Extract Structured Data
**POST** `/extract`

Extract structured data from documents based on the specified document type.

**Parameters:**
- `file` (form-data): Document file (PDF, JPG, JPEG, PNG)
- `document_type` (form-data): One of:
  - `Invoice`
  - `Form` 
  - `BusinessCard`
  - `TenderDocument`
  - `Person`
  - `TranslateText`

**Example Response:**
```json
{
  "success": true,
  "document_type": "Invoice",
  "filename": "sample_invoice.pdf",
  "data": {
    "invoice_number": "INV-2024-001",
    "date": "2024-01-15",
    "total_gross_worth": 1250.00,
    "items": [
      {
        "description": "Professional Services",
        "quantity": 10.0,
        "gross_worth": 1250.00
      }
    ]
  }
}
```

### 2. Extract and Translate Text
**POST** `/translate`

Extract text from documents and translate to English.

**Parameters:**
- `file` (form-data): Document file (PDF, JPG, JPEG, PNG)

**Example Response:**
```json
{
  "success": true,
  "filename": "document.pdf",
  "extracted_text": "Original text in source language...",
  "translated_text": "Translated text in English...",
  "detected_language": "auto-detected",
  "token_count": 1250
}
```

### 3. Get Supported Document Types
**GET** `/supported-types`

Returns list of all supported document types with descriptions.

### 4. Health Check
**GET** `/health`

Basic health check endpoint.

### 5. API Information
**GET** `/`

Returns API information and available endpoints.

## Frontend Integration Example

### JavaScript/Fetch Example

```javascript
// Extract structured data from invoice
async function extractInvoiceData(file) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', 'Invoice');

    try {
        const response = await fetch('http://localhost:8000/extract', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('Extracted data:', result.data);
            return result.data;
        } else {
            console.error('Extraction failed:', result.error);
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
}

// Extract and translate text
async function translateDocument(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:8000/translate', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('Translated text:', result.translated_text);
            return result;
        } else {
            console.error('Translation failed:', result.error);
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
}
```

### React Example

```jsx
import React, { useState } from 'react';

function DocumentUploader() {
    const [file, setFile] = useState(null);
    const [documentType, setDocumentType] = useState('Invoice');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);
        formData.append('document_type', documentType);

        try {
            const response = await fetch('http://localhost:8000/extract', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="file"
                    accept=".pdf,.jpg,.jpeg,.png"
                    onChange={(e) => setFile(e.target.files[0])}
                    required
                />
                
                <select
                    value={documentType}
                    onChange={(e) => setDocumentType(e.target.value)}
                >
                    <option value="Invoice">Invoice</option>
                    <option value="BusinessCard">Business Card</option>
                    <option value="TenderDocument">Tender Document</option>
                    <option value="Form">Form</option>
                    <option value="Person">Person</option>
                </select>
                
                <button type="submit" disabled={loading}>
                    {loading ? 'Processing...' : 'Extract Data'}
                </button>
            </form>
            
            {result && (
                <div>
                    <h3>Results:</h3>
                    <pre>{JSON.stringify(result, null, 2)}</pre>
                </div>
            )}
        </div>
    );
}

export default DocumentUploader;
```

## Error Handling

The API returns appropriate HTTP status codes:

- **200**: Success
- **400**: Bad Request (invalid file type, missing parameters)
- **401**: Unauthorized (invalid API key)
- **413**: Payload Too Large (file too big)
- **429**: Too Many Requests (rate limit exceeded)
- **500**: Internal Server Error

Error response format:
```json
{
  "success": false,
  "error": "Error message",
  "detail": "Additional error details"
}
```

## Configuration

Key configuration options in `config.py`:

- `MAX_FILE_SIZE`: Maximum upload file size (default: 10MB)
- `ALLOWED_FILE_EXTENSIONS`: Supported file types
- `GEMINI_MODEL_ID`: Google Gemini model to use
- `DEFAULT_TARGET_LANGUAGE`: Default translation target language

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Adding New Document Types

1. Define a new Pydantic model in `models.py`
2. Add the model to the mapping in `main.py`
3. Update the `DocumentType` enum
4. Update the supported types endpoint

### Testing

Use the interactive API documentation at `http://localhost:8000/docs` to test all endpoints.

## Deployment

For production deployment:

1. Set up proper environment variables
2. Configure CORS origins appropriately
3. Use a production WSGI server like Gunicorn
4. Set up proper logging and monitoring
5. Consider using a reverse proxy like Nginx

Example production command:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Troubleshooting

### Common Issues

1. **"Authentication failed"**: Check your GEMINI_API_KEY in .env file
2. **"Import errors"**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **"File too large"**: Check MAX_FILE_SIZE setting or reduce file size
4. **"Invalid file type"**: Ensure file extension is .pdf, .jpg, .jpeg, or .png

### Logging

The application logs important events and errors. Check the console output for detailed information when troubleshooting issues.

## License

This project is provided as-is for demonstration purposes.

## Support

For issues and questions, please refer to the FastAPI documentation and Google Gemini AI documentation.