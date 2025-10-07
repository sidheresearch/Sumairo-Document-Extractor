import React from 'react';
import { DOCUMENT_TYPES, DOCUMENT_TYPE_DESCRIPTIONS } from '../services/api';
import { FileText, CreditCard, Building, User, Languages, FileImage, FileSignature, FileBadge, FileCheck2, ShoppingCart } from 'lucide-react';

const DocumentTypeSelector = ({ selectedType, onTypeChange, loading }) => {
  const getIcon = (type) => {
    switch (type) {
      case DOCUMENT_TYPES.INVOICE:
        return <FileText className="w-5 h-5" />;
      case DOCUMENT_TYPES.BUSINESS_CARD:
        return <CreditCard className="w-5 h-5" />;
      case DOCUMENT_TYPES.TENDER_DOCUMENT:
        return <Building className="w-5 h-5" />;
      case DOCUMENT_TYPES.FORM:
        return <FileBadge className="w-5 h-5" />;
      case DOCUMENT_TYPES.PERSON:
        return <User className="w-5 h-5" />;
      case DOCUMENT_TYPES.PURCHASE_ORDER:
        return <ShoppingCart className="w-5 h-5" />;
      case DOCUMENT_TYPES.LC_DETAILS:
        return <FileSignature className="w-5 h-5" />;
      case DOCUMENT_TYPES.DOCUMENTARY_CREDIT:
        return <FileCheck2 className="w-5 h-5" />;
      case DOCUMENT_TYPES.LC1:
        return <FileBadge className="w-5 h-5" />;
      case DOCUMENT_TYPES.TRANSLATE_TEXT:
        return <Languages className="w-5 h-5" />;
      default:
        return <FileImage className="w-5 h-5" />;
    }
  };

  const types = [
    {
      value: DOCUMENT_TYPES.INVOICE,
      label: 'Invoice',
      description: DOCUMENT_TYPE_DESCRIPTIONS[DOCUMENT_TYPES.INVOICE]
    },
    {
      value: DOCUMENT_TYPES.BUSINESS_CARD,
      label: 'Business Card',
      description: DOCUMENT_TYPE_DESCRIPTIONS[DOCUMENT_TYPES.BUSINESS_CARD]
    },
    {
      value: DOCUMENT_TYPES.TENDER_DOCUMENT,
      label: 'Tender Document',
      description: DOCUMENT_TYPE_DESCRIPTIONS[DOCUMENT_TYPES.TENDER_DOCUMENT]
    },
    {
      value: DOCUMENT_TYPES.FORM,
      label: 'Form',
      description: DOCUMENT_TYPE_DESCRIPTIONS[DOCUMENT_TYPES.FORM]
    },
    {
      value: DOCUMENT_TYPES.PERSON,
      label: 'Person Info',
      description: DOCUMENT_TYPE_DESCRIPTIONS[DOCUMENT_TYPES.PERSON]
    },
    {
      value: DOCUMENT_TYPES.PURCHASE_ORDER,
      label: 'Purchase Order',
      description: DOCUMENT_TYPE_DESCRIPTIONS[DOCUMENT_TYPES.PURCHASE_ORDER]
    },
    {
      value: DOCUMENT_TYPES.LC_DETAILS,
      label: 'LC Details',
      description: DOCUMENT_TYPE_DESCRIPTIONS[DOCUMENT_TYPES.LC_DETAILS]
    },
    {
      value: DOCUMENT_TYPES.DOCUMENTARY_CREDIT,
      label: 'Documentary Credit',
      description: DOCUMENT_TYPE_DESCRIPTIONS[DOCUMENT_TYPES.DOCUMENTARY_CREDIT]
    },
    {
      value: DOCUMENT_TYPES.LC1,
      label: 'LC1',
      description: DOCUMENT_TYPE_DESCRIPTIONS[DOCUMENT_TYPES.LC1]
    },
    {
      value: DOCUMENT_TYPES.TRANSLATE_TEXT,
      label: 'Translate Text',
      description: DOCUMENT_TYPE_DESCRIPTIONS[DOCUMENT_TYPES.TRANSLATE_TEXT]
    }
  ];

  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-3">
        Document Type
      </label>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {types.map((type) => (
          <label
            key={type.value}
            className={`
              relative flex items-start p-4 border rounded-lg cursor-pointer
              transition-all duration-200 hover:shadow-md
              ${selectedType === type.value
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                : 'border-gray-200 hover:border-gray-300'
              }
              ${loading ? 'opacity-50 cursor-not-allowed' : ''}
            `}
          >
            <input
              type="radio"
              name="documentType"
              value={type.value}
              checked={selectedType === type.value}
              onChange={(e) => onTypeChange(e.target.value)}
              disabled={loading}
              className="sr-only"
            />
            <div className="flex items-center space-x-3 w-full">
              <div className={`
                flex-shrink-0 ${selectedType === type.value ? 'text-blue-600' : 'text-gray-400'}
              `}>
                {getIcon(type.value)}
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <h3 className={`
                    text-sm font-medium
                    ${selectedType === type.value ? 'text-blue-900' : 'text-gray-900'}
                  `}>
                    {type.label}
                  </h3>
                  {selectedType === type.value && (
                    <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                  )}
                </div>
                <p className={`
                  text-xs mt-1
                  ${selectedType === type.value ? 'text-blue-700' : 'text-gray-500'}
                `}>
                  {type.description}
                </p>
              </div>
            </div>
          </label>
        ))}
      </div>
    </div>
  );
};

export default DocumentTypeSelector;