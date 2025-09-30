import React from 'react';
import { CheckCircle, AlertCircle, FileText, Copy, Download } from 'lucide-react';
import { toast } from 'react-toastify';

const ResultDisplay = ({ result, error }) => {
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      toast.success('Copied to clipboard!');
    }).catch(() => {
      toast.error('Failed to copy to clipboard');
    });
  };

  const downloadJson = (data, filename) => {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${filename}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    toast.success('File downloaded!');
  };

  const formatValue = (value) => {
    if (typeof value === 'object' && value !== null) {
      return JSON.stringify(value, null, 2);
    }
    return String(value);
  };

  const renderDataTable = (data) => {
    if (!data || typeof data !== 'object') {
      return <pre className="text-sm bg-gray-50 p-3 rounded overflow-x-auto">{formatValue(data)}</pre>;
    }

    return (
      <div className="space-y-4">
        {Object.entries(data).map(([key, value]) => (
          <div key={key} className="border-b border-gray-100 pb-3 last:border-b-0">
            <dt className="text-sm font-medium text-gray-600 capitalize mb-1">
              {key.replace(/_/g, ' ')}
            </dt>
            <dd className="text-sm text-gray-900">
              {Array.isArray(value) ? (
                <div className="space-y-2">
                  {value.map((item, index) => (
                    <div key={index} className="bg-gray-50 p-3 rounded-lg">
                      {typeof item === 'object' ? (
                        <pre className="text-xs">{JSON.stringify(item, null, 2)}</pre>
                      ) : (
                        <span>{item}</span>
                      )}
                    </div>
                  ))}
                </div>
              ) : typeof value === 'object' && value !== null ? (
                <pre className="text-xs bg-gray-50 p-2 rounded overflow-x-auto">
                  {JSON.stringify(value, null, 2)}
                </pre>
              ) : (
                <span className="break-words">{String(value)}</span>
              )}
            </dd>
          </div>
        ))}
      </div>
    );
  };

  if (error) {
    return (
      <div className="result-card border border-red-200 rounded-lg p-6 bg-red-50">
        <div className="flex items-center space-x-3 mb-4">
          <AlertCircle className="w-6 h-6 text-red-500 flex-shrink-0" />
          <h3 className="text-lg font-semibold text-red-900">Error</h3>
        </div>
        <p className="text-red-800 leading-relaxed">{error}</p>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  return (
    <div className="result-card border border-green-200 rounded-lg p-6 bg-green-50">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <CheckCircle className="w-6 h-6 text-green-500" />
          <h3 className="text-lg font-semibold text-green-900">
            Extraction Successful
          </h3>
        </div>
        <div className="flex space-x-2">
          {result.data && (
            <>
              <button
                onClick={() => copyToClipboard(JSON.stringify(result.data, null, 2))}
                className="flex items-center space-x-1 px-3 py-1 text-sm text-green-700 hover:text-green-900 transition-colors"
                title="Copy to clipboard"
              >
                <Copy className="w-4 h-4" />
                <span>Copy</span>
              </button>
              <button
                onClick={() => downloadJson(result.data, `extracted-${result.document_type || 'data'}`)}
                className="flex items-center space-x-1 px-3 py-1 text-sm text-green-700 hover:text-green-900 transition-colors"
                title="Download JSON"
              >
                <Download className="w-4 h-4" />
                <span>Download</span>
              </button>
            </>
          )}
        </div>
      </div>

      {/* File info */}
      <div className="mb-4 pb-4 border-b border-green-200">
        <div className="flex items-center space-x-2 text-sm text-green-800">
          <FileText className="w-4 h-4" />
          <span><strong>File:</strong> {result.filename}</span>
          {result.document_type && (
            <>
              <span>•</span>
              <span><strong>Type:</strong> {result.document_type}</span>
            </>
          )}
          {result.token_count && (
            <>
              <span>•</span>
              <span><strong>Tokens:</strong> {result.token_count}</span>
            </>
          )}
        </div>
      </div>

      {/* Results */}
      <div className="space-y-4">
        {/* Translation results */}
        {result.extracted_text && (
          <div>
            <h4 className="text-md font-medium text-green-900 mb-2">Original Text</h4>
            <div className="bg-white p-4 rounded border">
              <pre className="text-sm whitespace-pre-wrap break-words">{result.extracted_text}</pre>
            </div>
          </div>
        )}
        
        {result.translated_text && (
          <div>
            <h4 className="text-md font-medium text-green-900 mb-2">
              Translated Text 
              {result.detected_language && (
                <span className="text-sm text-green-700 ml-2">
                  (from {result.detected_language})
                </span>
              )}
            </h4>
            <div className="bg-white p-4 rounded border">
              <pre className="text-sm whitespace-pre-wrap break-words">{result.translated_text}</pre>
            </div>
          </div>
        )}

        {/* Structured data results */}
        {result.data && (
          <div>
            <h4 className="text-md font-medium text-green-900 mb-2">Extracted Data</h4>
            <div className="bg-white p-4 rounded border">
              {renderDataTable(result.data)}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultDisplay;