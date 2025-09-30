import { useState, useCallback } from 'react';
import { documentAPI, validateFile } from '../services/api';

export const useDocumentExtractor = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const extractData = useCallback(async (file, documentType) => {
    try {
      setLoading(true);
      setError(null);
      setResult(null);

      // Validate file
      validateFile(file);

      // Extract data
      const response = await documentAPI.extractData(file, documentType);
      setResult(response);
      
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const translateText = useCallback(async (file) => {
    try {
      setLoading(true);
      setError(null);
      setResult(null);

      // Validate file
      validateFile(file);

      // Translate text
      const response = await documentAPI.translateText(file);
      setResult(response);
      
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setLoading(false);
    setResult(null);
    setError(null);
  }, []);

  return {
    loading,
    result,
    error,
    extractData,
    translateText,
    reset
  };
};