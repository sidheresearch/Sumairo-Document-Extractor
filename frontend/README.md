# Document Extractor Frontend

A modern React application for the Document Extractor API that provides an intuitive interface for extracting structured data from documents using AI.

## Features

- **🎯 Multiple Document Types**: Support for invoices, business cards, tender documents, forms, and person information
- **🌍 Translation**: Extract and translate text from documents in multiple languages
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **⚡ Real-time Processing**: Live updates and progress indicators
- **🎨 Modern UI**: Beautiful, clean interface built with Tailwind CSS
- **📋 Easy Export**: Copy to clipboard or download results as JSON
- **🔄 Drag & Drop**: Intuitive file upload with drag and drop support

## Prerequisites

- Node.js 16+ installed
- FastAPI backend running on `http://localhost:8000`

## Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   - Go to `http://localhost:3000`
   - The app should automatically open

## Usage

1. **Upload Document**: Drag and drop or click to upload PDF, JPG, or PNG files (max 10MB)
2. **Select Type**: Choose the type of document you're uploading
3. **Extract Data**: Click the extract button to process your document
4. **View Results**: See the structured data or translated text
5. **Export**: Copy or download the results

## Supported Document Types

- **Invoice**: Extract invoice numbers, dates, items, and totals
- **Business Card**: Extract contact information
- **Tender Document**: Extract comprehensive tender information
- **Form**: Extract form data and plan liabilities
- **Person Info**: Extract personal information and work topics
- **Translate Text**: Extract and translate text to English

## Environment Variables

Create a `.env` file in the frontend directory:

```bash
REACT_APP_API_URL=http://localhost:8000
```

## Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

## Technology Stack

- **React 18** - Modern React with hooks
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **React Dropzone** - File upload with drag & drop
- **React Toastify** - Toast notifications
- **Lucide React** - Beautiful icons

## Project Structure

```
src/
├── components/           # Reusable React components
│   ├── FileUpload.js    # File upload component
│   ├── DocumentTypeSelector.js
│   ├── ResultDisplay.js
│   └── LoadingSpinner.js
├── hooks/               # Custom React hooks
│   └── useDocumentExtractor.js
├── services/            # API service layer
│   └── api.js
├── App.js              # Main application component
├── index.js            # React entry point
└── index.css           # Global styles
```

## API Integration

The frontend communicates with the FastAPI backend through:

- **POST /extract** - Extract structured data
- **POST /translate** - Extract and translate text
- **GET /health** - Health check
- **GET /supported-types** - Get document types

## Error Handling

The app handles various error scenarios:

- **Network errors**: When the API is unreachable
- **File validation errors**: Invalid file types or sizes
- **API errors**: Rate limits, authentication, server errors
- **Service unavailable**: When AI model is overloaded

## Customization

### Styling
- Edit `tailwind.config.js` to customize the theme
- Modify `src/index.css` for global styles
- Component styles are in individual component files

### API Configuration
- Update `src/services/api.js` to modify API endpoints or add new ones
- Environment variables in `.env` file

### Adding New Document Types
1. Add the type to `DOCUMENT_TYPES` in `api.js`
2. Add description to `DOCUMENT_TYPE_DESCRIPTIONS`
3. Update the icon mapping in `DocumentTypeSelector.js`

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Ensure FastAPI backend is running on `http://localhost:8000`
   - Check CORS settings in the backend

2. **File Upload Fails**
   - Check file size (max 10MB)
   - Ensure file type is PDF, JPG, or PNG

3. **Build Fails**
   - Delete `node_modules` and `package-lock.json`
   - Run `npm install` again

4. **Styling Issues**
   - Ensure Tailwind CSS is properly configured
   - Check `postcss.config.js` settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.