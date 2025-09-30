from pydantic import BaseModel, Field
from typing import List, Optional

class Item(BaseModel):
    description: str = Field(description="The description of the item")
    quantity: float = Field(description="The Qty of the item")
    gross_worth: float = Field(description="The gross worth of the item")

class Invoice(BaseModel):
    """Extract the invoice number, date and all list items with description, quantity and gross worth and the total gross worth."""
    invoice_number: str = Field(description="The invoice number e.g. 1234567890")
    date: str = Field(description="The date of the invoice e.g. 2024-01-01")
    items: List[Item] = Field(description="The list of items with description, quantity and gross worth")
    total_gross_worth: float = Field(description="The total gross worth of the invoice")

class Form(BaseModel):
    """Extract the form number, fiscal start date, fiscal end date, and the plan liabilities beginning of the year and end of the year."""
    form_number: str = Field(description="The Form Number")
    start_date: str = Field(description="Effective Date")
    beginning_of_year: float = Field(description="The plan liabilities beginning of the year")
    end_of_year: float = Field(description="The plan liabilities end of the year")

class BusinessCard(BaseModel):
    """Extract information from a business card."""
    name: str = Field(description="The full name on the business card")
    title: str = Field(description="The job title on the business card")
    company: str = Field(description="The company name on the business card")
    phone: str = Field(description="The phone number on the business card")
    email: str = Field(description="The email address on the business card")
    website: str = Field(description="The website on the business card")
    address: str = Field(description="The address on the business card")

class TenderDocument(BaseModel):
    """Extract key information from a tender document."""
    tender_title: Optional[str] = Field(None, description="The title of the tender document.")
    tender_number: Optional[str] = Field(None, description="The unique identification number for the tender.")
    issuing_organization: Optional[str] = Field(None, description="The name of the organization issuing the tender.")
    submission_deadline: Optional[str] = Field(None, description="The deadline for submitting the tender proposal.")
    scope_of_work: Optional[str] = Field(None, description="A summary or description of the work to be performed.")
    scope_of_products_to_be_provided: Optional[str] = Field(None, description="A list of products or services to be provided.")
    eligibility_criteria: Optional[str] = Field(None, description="The requirements or qualifications bidders must meet.")
    submission_instructions: Optional[str] = Field(None, description="Instructions on how to prepare and submit the proposal.")
    general_terms_and_conditions_summary: Optional[str] = Field(None, description="summary of key general terms and conditions")
    specific_terms_and_conditions_summary: Optional[str] = Field(None, description="summary of key specific terms and conditions")
    contact_person: Optional[str] = Field(None, description="The name of the contact person for inquiries.")
    contact_information: Optional[str] = Field(None, description="Contact details (phone, email, address) for inquiries.")
    evaluation_criteria: Optional[str] = Field(None, description="The criteria used to evaluate the submitted proposals.")
    required_documents: Optional[List[str]] = Field(None, description="A list of documents that must be included in the submission.")
    site_visit_details: Optional[str] = Field(None, description="Information about any mandatory or optional site visits.")
    earnest_money_deposit_terms: Optional[str] = Field(None, description="Details regarding the earnest money deposit.")
    emd_terms: Optional[str] = Field(None, description="Details regarding the terms of the earnest money deposit.")
    payment_terms: Optional[str] = Field(None, description="Details regarding payment schedules and terms.")
    contract_duration: Optional[str] = Field(None, description="The expected duration of the contract.")

class Topic(BaseModel):
    name: str = Field(description="The name of the topic")

class Person(BaseModel):
    first_name: str = Field(description="The first name of the person")
    last_name: str = Field(description="The last name of the person")
    age: int = Field(description="The age of the person, if not provided please return 0")
    work_topics: List[Topic] = Field(description="The fields of interest of the person, if not provided please return an empty list")

# Response models for API
class ExtractionResponse(BaseModel):
    success: bool
    document_type: str
    filename: str
    data: dict

class TranslationResponse(BaseModel):
    success: bool
    filename: str
    extracted_text: Optional[str]
    translated_text: Optional[str]
    detected_language: Optional[str]
    token_count: Optional[int]

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None



    