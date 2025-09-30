import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner = ({ message = 'Processing document...', subMessage }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 bg-white rounded-lg card-shadow border">
      <Loader2 className="w-8 h-8 text-blue-500 animate-spin mb-4" />
      <h3 className="text-lg font-medium text-gray-900 mb-2">{message}</h3>
      {subMessage && (
        <p className="text-sm text-gray-600 text-center max-w-md">{subMessage}</p>
      )}
      <div className="mt-4 w-full max-w-xs">
        <div className="bg-gray-200 rounded-full h-2">
          <div className="bg-blue-500 h-2 rounded-full animate-pulse" style={{width: '60%'}}></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;