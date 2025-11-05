from sqlmodel import Field, SQLModel, Session, select
from typing import Optional, List
from enum import Enum
from datetime import date
from pydantic import field_validator, ValidationError, model_validator
import re
from utils.validations import (
    validate_uppercase,
    validate_cnic,
    validate_kin_cnic,
    validate_date_format,
    validate_postal_code,
    validate_contact,
    validate_email,
    validate_account_number,
    validate_iban
)


class AccountType(Enum):
    CURRENT = "CURRENT"
    SAVINGS = "SAVINGS"
    AHU_LAT = "AHU_LAT"


class MaritalStatus(Enum):
    SINGLE = "SINGLE"
    MARRIED = "MARRIED"
    DIVORCED = "DIVORCED"
    WIDOWED = "WIDOWED"


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class Occupation(Enum):
    SERVICE_GOVT = "SERVICE_GOVT"
    SERVICE_PRIVATE = "SERVICE_PRIVATE"
    FARMER = "FARMER"
    HOUSE_WIFE = "HOUSE_WIFE"
    STUDENT = "STUDENT"
    OTHER = "OTHER"


class ResidentialStatus(Enum):
    HOUSE_OWNED = "HOUSE_OWNED"
    RENTAL = "RENTAL"
    FAMILY = "FAMILY"
    OTHER = "OTHER"


class Item(SQLModel, table=True):
    """Item model for database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None


class AccountApplicationCreate(SQLModel):
    """Account Application Create Schema (without auto-generated fields)"""
    title_of_account: str  # Required, in block letters
    name_on_card: Optional[str] = None

    # Personal Information
    name: str  # As per CNIC, in block letters
    fathers_husbands_name: Optional[str] = None
    mothers_name: Optional[str] = None
    marital_status: Optional[MaritalStatus] = None
    gender: Optional[Gender] = None
    nationality: Optional[str] = None
    place_of_birth: Optional[str] = None
    date_of_birth: Optional[str] = None
    cnic_no: str  # Required
    cnic_expiry_date: Optional[str] = None

    # Address
    house_no_block_street: Optional[str] = None
    area_location: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None

    # Occupation
    occupation: Optional[Occupation] = None
    occupation_other: Optional[str] = None  # For OTHER occupation

    # Financial Info
    purpose_of_account: Optional[str] = None
    source_of_income: Optional[str] = None
    expected_monthly_turnover_dr: Optional[float] = None  # In Rs (M)
    expected_monthly_turnover_cr: Optional[float] = None  # In Rs (M)

    # Residential Status
    residential_status: Optional[ResidentialStatus] = None
    residential_status_other: Optional[str] = None  # For OTHER
    residing_since: Optional[str] = None  # Could be date or string

    # Next of Kin
    next_of_kin_name: Optional[str] = None
    next_of_kin_relation: Optional[str] = None  # S,W,D/O
    next_of_kin_cnic: Optional[str] = None
    next_of_kin_relationship: Optional[str] = None
    next_of_kin_contact_no: Optional[str] = None
    next_of_kin_address: Optional[str] = None
    next_of_kin_email: Optional[str] = None

    # Services Required
    internet_banking: bool = Field(default=False)
    mobile_banking: bool = Field(default=False)
    check_book: bool = Field(default=False)
    sms_alerts: bool = Field(default=False)

    # Card Type
    card_type_gold: bool = Field(default=False)
    card_type_classic: bool = Field(default=False)

    # Zakat Deduction
    zakat_deduction: bool = Field(default=False)

    # Field validators (same as AccountApplication)
    @field_validator('name', 'title_of_account', 'fathers_husbands_name', 'mothers_name', 'nationality', 'place_of_birth', 'house_no_block_street', 'area_location', 'city', 'purpose_of_account', 'source_of_income', 'next_of_kin_name', 'next_of_kin_address', 'occupation_other', 'residential_status_other', 'name_on_card')
    @classmethod
    def validate_uppercase_fields(cls, v):
        return validate_uppercase(v)

    @field_validator('cnic_no')
    @classmethod
    def validate_cnic_field(cls, v):
        return validate_cnic(v)

    @field_validator('next_of_kin_cnic')
    @classmethod
    def validate_kin_cnic_field(cls, v):
        return validate_kin_cnic(v)

    @field_validator('date_of_birth', 'cnic_expiry_date')
    @classmethod
    def validate_date_fields(cls, v):
        return validate_date_format(v)

    @field_validator('postal_code')
    @classmethod
    def validate_postal_code_field(cls, v):
        return validate_postal_code(v)

    @field_validator('next_of_kin_contact_no')
    @classmethod
    def validate_contact_field(cls, v):
        return validate_contact(v)

    @field_validator('next_of_kin_email')
    @classmethod
    def validate_email_field(cls, v):
        return validate_email(v)

    @model_validator(mode='after')
    def validate_next_of_kin_details(self) -> 'AccountApplication':
        """Validate that if any next of kin field is provided, required fields are present"""
        kin_fields = [
            self.next_of_kin_name,
            self.next_of_kin_relation,
            self.next_of_kin_cnic,
            self.next_of_kin_relationship,
            self.next_of_kin_contact_no,
            self.next_of_kin_address,
            self.next_of_kin_email
        ]

        # Check if any next of kin field is provided
        has_any_kin_info = any(field is not None and field != "" for field in kin_fields)

        if has_any_kin_info:
            # If any kin info is provided, require essential fields
            if not self.next_of_kin_name:
                raise ValueError("Next of kin name is required when providing next of kin information")
            if not self.next_of_kin_relation:
                raise ValueError("Next of kin relation is required when providing next of kin information")
            if not self.next_of_kin_cnic:
                raise ValueError("Next of kin CNIC is required when providing next of kin information")

        return self

    @model_validator(mode='after')
    def validate_next_of_kin_details_create(self) -> 'AccountApplicationCreate':
        """Validate that if any next of kin field is provided, required fields are present"""
        kin_fields = [
            self.next_of_kin_name,
            self.next_of_kin_relation,
            self.next_of_kin_cnic,
            self.next_of_kin_relationship,
            self.next_of_kin_contact_no,
            self.next_of_kin_address,
            self.next_of_kin_email
        ]

        # Check if any next of kin field is provided
        has_any_kin_info = any(field is not None and field != "" for field in kin_fields)

        if has_any_kin_info:
            # If any kin info is provided, require essential fields
            if not self.next_of_kin_name:
                raise ValueError("Next of kin name is required when providing next of kin information")
            if not self.next_of_kin_relation:
                raise ValueError("Next of kin relation is required when providing next of kin information")
            if not self.next_of_kin_cnic:
                raise ValueError("Next of kin CNIC is required when providing next of kin information")

        return self

    @model_validator(mode='after')
    def validate_account_title_name_consistency(self) -> 'AccountApplicationCreate':
        """Validate that title_of_account, name, and name_on_card are identical"""
        # Since title_of_account and name are required, they must be equal
        if self.title_of_account != self.name:
            raise ValueError("Account title and name must be identical")
        
        # If name_on_card is provided, it must match name (and thus title_of_account)
        if self.name_on_card is not None and self.name_on_card != self.name:
            raise ValueError("Card name must be identical to account name and title")
        
        return self
    """Account Application Form Schema"""
    id: Optional[int] = Field(default=None, primary_key=True)
    account_no: Optional[str] = None  # Auto-generated if not provided (12 digits)
    date: Optional[str] = None
    iban: Optional[str] = None  # Auto-generated if not provided (PK + 18 digits)
    branch_city: Optional[str] = None
    branch_code: Optional[str] = None
    sbp_code: Optional[str] = None
    account_type: Optional[AccountType] = None
    title_of_account: str  # Required, in block letters
    name_on_card: Optional[str] = None

    # Personal Information
    name: str  # As per CNIC, in block letters
    fathers_husbands_name: Optional[str] = None
    mothers_name: Optional[str] = None
    marital_status: Optional[MaritalStatus] = None
    gender: Optional[Gender] = None
    nationality: Optional[str] = None
    place_of_birth: Optional[str] = None
    date_of_birth: Optional[str] = None
    cnic_no: str  # Required
    cnic_expiry_date: Optional[str] = None

    # Address
    house_no_block_street: Optional[str] = None
    area_location: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None

    # Occupation
    occupation: Optional[Occupation] = None
    occupation_other: Optional[str] = None  # For OTHER occupation

    # Financial Info
    purpose_of_account: Optional[str] = None
    source_of_income: Optional[str] = None
    expected_monthly_turnover_dr: Optional[float] = None  # In Rs (M)
    expected_monthly_turnover_cr: Optional[float] = None  # In Rs (M)

    # Residential Status
    residential_status: Optional[ResidentialStatus] = None
    residential_status_other: Optional[str] = None  # For OTHER
    residing_since: Optional[str] = None  # Could be date or string

    # Next of Kin
    next_of_kin_name: Optional[str] = None
    next_of_kin_relation: Optional[str] = None  # S,W,D/O
    next_of_kin_cnic: Optional[str] = None
    next_of_kin_relationship: Optional[str] = None
    next_of_kin_contact_no: Optional[str] = None
    next_of_kin_address: Optional[str] = None
    next_of_kin_email: Optional[str] = None

    # Services Required
    internet_banking: bool = Field(default=False)
    mobile_banking: bool = Field(default=False)
    check_book: bool = Field(default=False)
    sms_alerts: bool = Field(default=False)

    # Card Type
    card_type_gold: bool = Field(default=False)
    card_type_classic: bool = Field(default=False)

    # Zakat Deduction
    zakat_deduction: bool = Field(default=False)

    @field_validator('name', 'title_of_account', 'fathers_husbands_name', 'mothers_name', 'nationality', 'place_of_birth', 'house_no_block_street', 'area_location', 'city', 'purpose_of_account', 'source_of_income', 'next_of_kin_name', 'next_of_kin_address', 'occupation_other', 'residential_status_other', 'name_on_card')
    @classmethod
    def validate_uppercase_fields_full(cls, v):
        return validate_uppercase(v)

    @field_validator('cnic_no')
    @classmethod
    def validate_cnic_field_full(cls, v):
        return validate_cnic(v)

    @field_validator('next_of_kin_cnic')
    @classmethod
    def validate_kin_cnic_field_full(cls, v):
        return validate_kin_cnic(v)

    @field_validator('date', 'date_of_birth', 'cnic_expiry_date')
    @classmethod
    def validate_date_fields_full(cls, v):
        return validate_date_format(v)

    @field_validator('postal_code')
    @classmethod
    def validate_postal_code_field_full(cls, v):
        return validate_postal_code(v)

    @field_validator('next_of_kin_contact_no')
    @classmethod
    def validate_contact_field_full(cls, v):
        return validate_contact(v)

    @field_validator('account_no')
    @classmethod
    def validate_account_number_field_full(cls, v):
        return validate_account_number(v)

    @field_validator('iban')
    @classmethod
    def validate_iban_field_full(cls, v):
        return validate_iban(v)

    @model_validator(mode='after')
    def validate_account_title_name_consistency_full(self) -> 'AccountApplication':
        """Validate that title_of_account, name, and name_on_card are identical"""
        # Since title_of_account and name are required, they must be equal
        if self.title_of_account != self.name:
            raise ValueError("Account title and name must be identical")
        
        # If name_on_card is provided, it must match name (and thus title_of_account)
        if self.name_on_card is not None and self.name_on_card != self.name:
            raise ValueError("Card name must be identical to account name and title")
        
        return self

    # SQL Query Methods
    @classmethod
    def get_all(cls, session: Session) -> List['AccountApplication']:
        """SQL Query: SELECT * FROM accountapplication"""
        return session.exec(select(cls)).all()

    @classmethod
    def get_by_id(cls, session: Session, application_id: int) -> Optional['AccountApplication']:
        """SQL Query: SELECT * FROM accountapplication WHERE id = ?"""
        return session.get(cls, application_id)

    @classmethod
    def create(cls, session: Session, application_data: 'AccountApplication') -> 'AccountApplication':
        """SQL Query: INSERT INTO accountapplication (...) VALUES (...)"""
        session.add(application_data)
        session.commit()
        session.refresh(application_data)
        return application_data

    @classmethod
    def update_by_id(cls, session: Session, application_id: int, update_data: dict) -> Optional['AccountApplication']:
        """SQL Query: UPDATE accountapplication SET ... WHERE id = ?"""
        application = session.get(cls, application_id)
        if not application:
            return None

        for field, value in update_data.items():
            if hasattr(application, field):
                setattr(application, field, value)

        session.commit()
        session.refresh(application)
        return application

    @classmethod
    def delete_by_id(cls, session: Session, application_id: int) -> bool:
        """SQL Query: DELETE FROM accountapplication WHERE id = ?"""
        application = session.get(cls, application_id)
        if not application:
            return False

        session.delete(application)
        session.commit()
        return True

    @classmethod
    def get_by_cnic(cls, session: Session, cnic_no: str) -> Optional['AccountApplication']:
        """SQL Query: SELECT * FROM accountapplication WHERE cnic_no = ?"""
        return session.exec(select(cls).where(cls.cnic_no == cnic_no)).first()

    @classmethod
    def get_by_account_type(cls, session: Session, account_type: AccountType) -> List['AccountApplication']:
        """SQL Query: SELECT * FROM accountapplication WHERE account_type = ?"""
        return session.exec(select(cls).where(cls.account_type == account_type)).all()

    @classmethod
    def get_by_city(cls, session: Session, city: str) -> List['AccountApplication']:
        """SQL Query: SELECT * FROM accountapplication WHERE city = ?"""
        return session.exec(select(cls).where(cls.city == city)).all()

    @classmethod
    def count_total(cls, session: Session) -> int:
        """SQL Query: SELECT COUNT(*) FROM accountapplication"""
        from sqlmodel import func
        return session.exec(select(func.count(cls.id))).one()

    @classmethod
    def get_paginated(cls, session: Session, skip: int = 0, limit: int = 10) -> List['AccountApplication']:
        """SQL Query: SELECT * FROM accountapplication LIMIT ? OFFSET ?"""
        return session.exec(select(cls).offset(skip).limit(limit)).all()

    @classmethod
    def get_by_account_number(cls, session: Session, account_no: str) -> Optional['AccountApplication']:
        """SQL Query: SELECT * FROM accountapplication WHERE account_no = ?"""
        return session.exec(select(cls).where(cls.account_no == account_no)).first()

    @classmethod
    def get_by_iban(cls, session: Session, iban: str) -> Optional['AccountApplication']:
        """SQL Query: SELECT * FROM accountapplication WHERE iban = ?"""
        return session.exec(select(cls).where(cls.iban == iban)).first()