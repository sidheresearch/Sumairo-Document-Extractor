import React, { useState, useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Brain, FileText, Zap, Globe, RefreshCw } from 'lucide-react';

import FileUpload from './components/FileUpload';
import DocumentTypeSelector from './components/DocumentTypeSelector';
import ResultDisplay from './components/ResultDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import { useDocumentExtractor } from './hooks/useDocumentExtractor';
import { DOCUMENT_TYPES, documentAPI } from './services/api';
import './index.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [documentType, setDocumentType] = useState(DOCUMENT_TYPES.INVOICE);
  const [isHealthy, setIsHealthy] = useState(null);
  
  const { loading, result, error, extractData, translateText, reset } = useDocumentExtractor();

  // Health check on component mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        await documentAPI.healthCheck();
        setIsHealthy(true);
      } catch (err) {
        setIsHealthy(false);
        console.error('Health check failed:', err);
      }
    };
    
    checkHealth();
  }, []);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    reset(); // Clear previous results
  };

  const handleFileRemove = () => {
    setSelectedFile(null);
    reset();
  };

  const handleExtract = async () => {
    if (!selectedFile) {
      toast.error('Please select a file first');
      return;
    }

    try {
      if (documentType === DOCUMENT_TYPES.TRANSLATE_TEXT) {
        await translateText(selectedFile);
      } else {
        await extractData(selectedFile, documentType);
      }
      toast.success('Document processed successfully!');
    } catch (err) {
      toast.error(err.message || 'An error occurred while processing the document');
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setDocumentType(DOCUMENT_TYPES.INVOICE);
    reset();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-500 rounded-lg">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Sumairo Document Extractor</h1>
                <p className="text-sm text-gray-500">AI-powered document analysis</p>
              </div>
            </div>
            
            {/* Health status */}
            <div className="flex items-center space-x-2">
              {isHealthy !== null && (
                <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
                  isHealthy ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  <div className={`w-2 h-2 rounded-full ${
                    isHealthy ? 'bg-green-500' : 'bg-red-500'
                  }`}></div>
                  <span>{isHealthy ? ' Online' : ' Offline'}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Features Banner */}
        <div className="mb-8 bg-white rounded-xl p-6 card-shadow">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Extract Structured Data from Any Document
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Upload your documents and let our AI extract structured information, 
              translate text, and organize data automatically .
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center p-4">
              <FileText className="w-8 h-8 text-blue-500 mx-auto mb-2" />
              <h3 className="font-medium text-gray-900">Multi-format</h3>
              <p className="text-sm text-gray-500">PDF, JPG, PNG</p>
            </div>
            <div className="text-center p-4">
              <Zap className="w-8 h-8 text-yellow-500 mx-auto mb-2" />
              <h3 className="font-medium text-gray-900">Fast Processing</h3>
              <p className="text-sm text-gray-500">AI-powered extraction</p>
            </div>
            <div className="text-center p-4">
              <Globe className="w-8 h-8 text-green-500 mx-auto mb-2" />
              <h3 className="font-medium text-gray-900">Translation</h3>
              <p className="text-sm text-gray-500">Multi-language support</p>
            </div>
            <div className="text-center p-4">
              <Brain className="w-8 h-8 text-purple-500 mx-auto mb-2" />
              <h3 className="font-medium text-gray-900">Smart Analysis</h3>
              <p className="text-sm text-gray-500">Structured output</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Input */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl p-6 card-shadow">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                1. Upload Document
              </h3>
              <FileUpload
                onFileSelect={handleFileSelect}
                selectedFile={selectedFile}
                onFileRemove={handleFileRemove}
                loading={loading}
              />
            </div>

            <div className="bg-white rounded-xl p-6 card-shadow">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                2. Select Document Type
              </h3>
              <DocumentTypeSelector
                selectedType={documentType}
                onTypeChange={setDocumentType}
                loading={loading}
              />
            </div>

            <div className="flex space-x-3">
              <button
                onClick={handleExtract}
                disabled={!selectedFile || loading}
                className="flex-1 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4" />
                    <span>
                      {documentType === DOCUMENT_TYPES.TRANSLATE_TEXT 
                        ? 'Extract & Translate' 
                        : 'Extract Data'
                      }
                    </span>
                  </>
                )}
              </button>
              
              <button
                onClick={handleReset}
                disabled={loading}
                className="px-6 py-3 border border-gray-300 hover:border-gray-400 disabled:border-gray-200 disabled:cursor-not-allowed text-gray-700 disabled:text-gray-400 font-medium rounded-lg transition-colors duration-200"
              >
                Reset
              </button>
            </div>
          </div>

          {/* Right Column - Output */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl p-6 card-shadow min-h-[400px]">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                3. Results
              </h3>
              
              {loading && (
                <LoadingSpinner 
                  message="Processing document..."
                  subMessage={
                    documentType === DOCUMENT_TYPES.TRANSLATE_TEXT
                      ? "Extracting and translating text from your document. This may take a few moments..."
                      : `Analyzing your ${documentType.toLowerCase()} and extracting structured data...`
                  }
                />
              )}
              
              {!loading && (result || error) && (
                <ResultDisplay result={result} error={error} />
              )}
              
              {!loading && !result && !error && (
                <div className="flex items-center justify-center h-64 text-gray-500">
                  <div className="text-center">
                    <FileText className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                    <p>Upload a document and click "Extract Data" to see results here</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-sm text-gray-500">
          <p>
            Powered by Google Gemini AI • 
            <a 
              href="http://localhost:8000/docs" 
              target="_blank" 
              rel="noopener noreferrer"
              className="ml-1 text-blue-500 hover:text-blue-700"
            >
              API Documentation
            </a>
          </p>
        </footer>
      </main>

      {/* Toast Container */}
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </div>
  );
}

export default App;