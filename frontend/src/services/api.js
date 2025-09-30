import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds timeout for file uploads
});

// Document types mapping
export const DOCUMENT_TYPES = {
  INVOICE: 'Invoice',
  FORM: 'Form',
  BUSINESS_CARD: 'BusinessCard',
  TENDER_DOCUMENT: 'TenderDocument',
  PERSON: 'Person',
  LC_DETAILS: 'LCDetails',
  DOCUMENTARY_CREDIT: 'DocumentaryCredit',
  LC1: 'LC1',
  TRANSLATE_TEXT: 'TranslateText'
};

// Document type descriptions
export const DOCUMENT_TYPE_DESCRIPTIONS = {
  [DOCUMENT_TYPES.INVOICE]: 'Extract invoice number, date, items, and total gross worth',
  [DOCUMENT_TYPES.FORM]: 'Extract form number, dates, and plan liabilities',
  [DOCUMENT_TYPES.BUSINESS_CARD]: 'Extract contact information from business cards',
  [DOCUMENT_TYPES.TENDER_DOCUMENT]: 'Extract comprehensive tender document information',
  [DOCUMENT_TYPES.PERSON]: 'Extract person information including name, age, and work topics',
  [DOCUMENT_TYPES.LC_DETAILS]: 'Extract details from a Letter of Credit document',
  [DOCUMENT_TYPES.DOCUMENTARY_CREDIT]: 'Extract all relevant information from a documentary credit application',
  [DOCUMENT_TYPES.LC1]: 'Extract all relevant information from a letter of credit application',
  [DOCUMENT_TYPES.TRANSLATE_TEXT]: 'Extract and translate text from documents'
};

class DocumentExtractorAPI {
  /**
   * Extract structured data from document
   */
  async extractData(file, documentType) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);

    try {
      const response = await apiClient.post('/extract', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          console.log(`Upload Progress: ${percentCompleted}%`);
        },
      });
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Extract and translate text from document
   */
  async translateText(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await apiClient.post('/translate', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          console.log(`Upload Progress: ${percentCompleted}%`);
        },
      });
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Get supported document types
   */
  async getSupportedTypes() {
    try {
      const response = await apiClient.get('/supported-types');
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Health check
   */
  async healthCheck() {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  /**
   * Handle API errors
   */
  handleError(error) {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          throw new Error(data.detail || 'Invalid request. Please check your file and document type.');
        case 401:
          throw new Error('Authentication failed. Please check API key configuration.');
        case 413:
          throw new Error('File too large. Maximum size allowed is 10MB.');
        case 429:
          throw new Error('Rate limit exceeded. Please try again later.');
        case 500:
          throw new Error(data.detail || 'Internal server error. Please try again later.');
        case 503:
          throw new Error('Service temporarily unavailable. The AI model is overloaded, please try again in a few minutes.');
        default:
          throw new Error(data.detail || `Server error: ${status}`);
      }
    } else if (error.request) {
      // Network error
      throw new Error('Network error. Please check if the server is running at ' + API_BASE_URL);
    } else {
      // Other error
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
}

// Export singleton instance
export const documentAPI = new DocumentExtractorAPI();

// Utility functions
export const validateFile = (file) => {
  const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
  const maxSize = 10 * 1024 * 1024; // 10MB

  if (!allowedTypes.includes(file.type)) {
    throw new Error('Invalid file type. Please upload PDF, JPG, or PNG files only.');
  }

  if (file.size > maxSize) {
    throw new Error('File too large. Maximum size allowed is 10MB.');
  }

  return true;
};

export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};