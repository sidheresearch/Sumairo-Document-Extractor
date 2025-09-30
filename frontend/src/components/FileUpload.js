import React, { useCallback } from 'react';
import DocumentTypeSelector from './DocumentTypeSelector';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, Image, X } from 'lucide-react';
import { formatFileSize } from '../services/api';

const FileUpload = ({ onFileSelect, selectedFile, onFileRemove, selectedType, onTypeChange, loading }) => {
  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0];
      let errorMessage = 'File rejected: ';
      
      if (rejection.errors.some(e => e.code === 'file-invalid-type')) {
        errorMessage += 'Invalid file type. Please upload PDF, JPG, or PNG files only.';
      } else if (rejection.errors.some(e => e.code === 'file-too-large')) {
        errorMessage += 'File too large. Maximum size is 10MB.';
      } else {
        errorMessage += rejection.errors[0].message;
      }
      
      alert(errorMessage);
      return;
    }

    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: false,
    disabled: loading
  });

  const getFileIcon = (file) => {
    if (file.type === 'application/pdf') {
      return <FileText className="w-8 h-8 text-red-500" />;
    }
    return <Image className="w-8 h-8 text-blue-500" />;
  };

  return (
    <div className="w-full space-y-6">
      <DocumentTypeSelector
        selectedType={selectedType}
        onTypeChange={onTypeChange}
        loading={loading}
      />
      {!selectedFile ? (
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
            upload-area card-shadow transition-all duration-300
            ${isDragActive ? 'drag-active border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
            ${isDragReject ? 'drag-reject border-red-400 bg-red-50' : ''}
            ${loading ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <input {...getInputProps()} />
          <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <p className="text-lg font-medium text-gray-900 mb-2">
            {isDragActive ? 'Drop the file here...' : 'Upload Document'}
          </p>
          <p className="text-sm text-gray-500 mb-4">
            Drag and drop a file here, or click to select
          </p>
          <p className="text-xs text-gray-400">
            Supported formats: PDF, JPG, PNG (Max 10MB)
          </p>
        </div>
      ) : (
        <div className="border border-gray-200 rounded-lg p-4 bg-white card-shadow">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              {getFileIcon(selectedFile)}
              <div>
                <p className="font-medium text-gray-900">{selectedFile.name}</p>
                <p className="text-sm text-gray-500">
                  {formatFileSize(selectedFile.size)} • {selectedFile.type}
                </p>
              </div>
            </div>
            <button
              onClick={onFileRemove}
              disabled={loading}
              className="p-2 text-gray-400 hover:text-red-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              title="Remove file"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;