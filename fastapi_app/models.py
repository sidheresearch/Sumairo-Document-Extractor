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


# Topic and Person
class Topic(BaseModel):
    name: str = Field(description="The name of the topic")

class Person(BaseModel):
    first_name: str = Field(description="The first name of the person")
    last_name: str = Field(description="The last name of the person")
    age: int = Field(description="The age of the person, if not provided please return 0")
    work_topics: List[Topic] = Field(description="The fields of interest of the person, if not provided please return an empty list")

# LCDetails Model
class LCDetails(BaseModel):
    lc_number: str = Field(..., description="Letter of Credit number")
    issue_date: Optional[str] = Field(None, description="Date of issue")
    expiry_date: Optional[str] = Field(None, description="Date of expiry")
    applicant_name: Optional[str] = Field(None, description="Name of the applicant")
    beneficiary_name: Optional[str] = Field(None, description="Name of the beneficiary")
    amount: Optional[float] = Field(None, description="Total LC amount in specified currency")
    currency: Optional[str] = Field(None, description="Currency of the LC")
    bank_name: Optional[str] = Field(None, description="Issuing bank name")
    bank_branch: Optional[str] = Field(None, description="Issuing bank branch")
    incoterms: Optional[str] = Field(None, description="Trade terms like FOB, CIF, etc.")
    hs_code: Optional[str] = Field(None, description="HS Code if mentioned")
    product_description: Optional[str] = Field(None, description="Quantity and description of goods/services")
    shipment_port: Optional[str] = Field(None, description="Port of shipment")
    destination_port: Optional[str] = Field(None, description="Port of destination")
    transport_mode: Optional[str] = Field(None, description="Mode of transport (e.g., Sea, Air)")
    document_requirements: Optional[str] = Field(None, description="Required documents under LC")
    additional_conditions: Optional[str] = Field(None, description="Any special conditions or clauses")

# Drafts, CreditAvailableBy, PartialShipments, Transhipments
from typing import Literal
class Drafts(BaseModel):
    selected_option: Literal["AT SIGHT", "90 DAYS FROM b/l date"] = Field(description="Indicates which option is selected by a checkmark.", alias = "42c")

class CreditAvailableBy(BaseModel):
    selected_option: Literal["ACCEPTANCE", "DEF PAYMENT", "NEGOTIATION", "SIGHT PAYMENT"] = Field(description="Indicates which option is selected by a checkmark.", alias = "41a")

class PartialShipments(BaseModel):
    selected_option: Literal["PROHIBITED", "PERMITTED"] = Field(description="Indicates which option is selected by a checkmark.", alias = "43p")

class Transhipments(BaseModel):
    selected_option: Literal["PROHIBITED", "PERMITTED"] = Field(description="Indicates which option is selected by a checkmark.", alias = "43T")

# LC1 Model
class LC1(BaseModel):
    lc_number: str = Field(..., description="Letter of Credit number")
    bank_name: Optional[str] = Field(None, description="Issuing bank name")
    bank_branch: Optional[str] = Field(None, description="Issuing bank branch")
    incoterms: Optional[str] = Field(None, description="Trade terms like FOB, CIF, etc.")
    type_of_LC: Optional[str] = Field(None, description="Type of LC", alias = "40A" )
    date_and_place_of_expiry: Optional[str] = Field(None, description="Date and Place of Expiry", alias = "31D" )
    applicant_name_and_address: Optional[str] = Field(None, description="Name and address of the applicant", alias = "50")
    beneficiary_name_and_address: Optional[str] = Field(None, description="Name and address of the beneficiary", alias = "59")
    currency_and_amount_of_credit: Optional[float] = Field(None, description="Total credit amount in specified currency, in words and figures", alias = "32B")
    currency: Optional[str] = Field(None, description="Currency of the LC")
    percentage_credit_amount_tolerance: Optional[str] = Field(None, description="Percentage credit amount tolerance", alias = "39A")
    maximum_credit_amount: Optional[float] = Field(None, description="Maximum credit amount", alias = "39B")
    additional_amounts_covered: Optional[str] = Field(None, description="Additional amounts covered (usance interest)", alias = "39C")
    credit_available_with: Optional[str] = Field(None, description="Credit available with", alias = "41a")
    credit_available_by: CreditAvailableBy
    drafts_at: Drafts
    partial_shipments: PartialShipments
    transhipments: Transhipments
    shipment_from: Optional[str] = Field(None, description="Port of shipment", alias = "44A")
    shipment_to: Optional[str] = Field(None, description="Port of destination", alias = "44B")
    latest_date_of_shipment: Optional[str] = Field(None, description="Latest date of shipment", alias = "44C")
    quantity_and_description_of_goods: Optional[str] = Field(None, description="Quantity and description of goods/services", alias = "45A")
    hs_code: Optional[str] = Field(None, description="HS Code if mentioned")
    import_license_or_OGL_details: Optional[str] = Field(None, description="Import license or OGL details")
    documents_required: Optional[List[str]] = Field(None, description="A list of documents that must be included in the submission.")
    additional_conditions: Optional[str] = Field(None, description="Any special conditions or clauses", alias = "47A:T")
    specify_if_any_charges_to_beneficiary_account: Optional[str] = Field(None, description="Specify if any charges to beneficiary account", alias = "71B")
    period_of_presentation_of_documents: Optional[str] = Field(None, description="Period of presentation of documents", alias = "48")
    confirmation_instructions: Optional[str] = Field(None, description="Confirmation instructions", alias = "49")
    advise_through_bank_name: Optional[str] = Field(None, description="Advise through bank name", alias = "57a")
    sender_receiver_information: Optional[str] = Field(None, description="Reimbursement bank name", alias = "72")
    class config:
        validate_by_name = True

# Nested models for DocumentaryCredit
class ApplicantDetails(BaseModel):
    name: str = Field(..., alias="50")
    bank_bic: str = Field(..., alias="51A")
    full_address: str = Field(..., alias="47A")

class BeneficiaryDetails(BaseModel):
    name: str = Field(..., alias="59_name")
    address: str = Field(..., alias="59_address")

class ShipmentDetails(BaseModel):
    draft_terms: str = Field(..., alias="42C")
    drawn_on: str = Field(..., alias="42D")
    partial_shipments: str = Field(..., alias="43P")
    transhipment: str = Field(..., alias="43T")
    loading_port: str = Field(..., alias="44A")
    discharge_port: str = Field(..., alias="44E")
    latest_shipment_date: Optional[str] = Field(None, alias="44F")
    goods_description: str = Field(..., alias="45A")
    additional_conditions: Optional[str] = Field(None, alias="45B")
    incoterms: Optional[str] = Field(None, alias="46A")

class ComplianceRequirements(BaseModel):
    language: str
    quantity_tolerance: str
    required_documents: List[str]
    vessel_requirements: Optional[str]
    shipment_constraints: List[str]
    document_format_rules: Optional[str]
    communication_instructions: Optional[str]

class PresentationTerms(BaseModel):
    hs_code: Optional[str] = Field(None, description="HS code to be shown on B/L")
    commingled_quantity_note: Optional[str] = Field(None, description="B/L must show commingled quantity")
    liability_clause: Optional[str] = Field(None, description="Force majeure and regulatory disclaimer")
    presentation_period_days: Optional[int] = Field(None, alias="48", description="Days allowed for document presentation")
    discrepancy_fee_usd: Optional[float] = Field(None, description="Fee charged for discrepant documents")
    swift_routing: Optional[str] = Field(None, description="SWIFT address for routing discrepant documents")
    applicable_rules: Optional[List[str]] = Field(None, description="Applicable ICC rules")
    charge_distribution: Optional[List[str]] = Field(None, description="Who bears charges inside/outside India")
    confirmation_instruction: Optional[str] = Field(None, alias="49")
    reimbursing_bank_bic: Optional[str] = Field(None, alias="53A")
    negotiation_instruction: Optional[str] = Field(None, alias="78")

class DocumentaryCredit(BaseModel):
    sequence_of_total: str = Field(..., alias="27")
    form_of_credit: str = Field(..., alias="40A")
    credit_number: str = Field(..., alias="20")
    date_of_issue: Optional[str] = Field(None, alias="31C")
    applicable_rules: str = Field(..., alias="40E")
    expiry_date: Optional[str] = Field(None, alias="31D_date")
    expiry_place: str = Field(..., alias="31D_place")
    currency: str = Field(..., alias="32B")
    amount: Optional[float] = Field(None, alias="amount")
    percentage_tolerance: str = Field(..., alias="39A")
    applicant: ApplicantDetails
    beneficiary: BeneficiaryDetails
    shipment_details: ShipmentDetails
    compliance: ComplianceRequirements
    presentation_terms: PresentationTerms
    class Config:
        validate_by_name = True

class BankingInstructions(BaseModel):
    non_negotiable_doc_routing: str = Field(..., description="Instructions for sending non-negotiable documents")
    reimbursement_bank: str = Field(..., description="Bank to draw reimbursement from")
    reimbursement_notice_days: Optional[int] = Field(None, description="Notice period before reimbursement")
    advise_through_bic: Optional[str] = Field(None, alias="57A", description="BIC of advise-through bank")
    swift_ack_instruction: Optional[str] = Field(None, alias="72Z", description="SWIFT acknowledgment instruction")

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



    