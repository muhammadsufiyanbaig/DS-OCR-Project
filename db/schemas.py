from sqlmodel import Field, SQLModel, Session, select
from typing import Optional, List
from enum import Enum as PyEnum
from sqlalchemy import Enum
from datetime import date
from pydantic import field_validator, model_validator, ValidationError
import re
from utils.validations import (
    validate_uppercase,
    validate_cnic,
    validate_kin_cnic,
    validate_date_format,
    validate_postal_code,
    validate_contact,
    validate_email
)


class AccountType(PyEnum):
    CURRENT = "CURRENT"
    SAVINGS = "SAVINGS"
    AHU_LAT = "AHU_LAT"


class MaritalStatus(PyEnum):
    SINGLE = "SINGLE"
    MARRIED = "MARRIED"
    DIVORCED = "DIVORCED"
    WIDOWED = "WIDOWED"


class Gender(PyEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class Occupation(PyEnum):
    SERVICE_GOVT = "SERVICE_GOVT"
    SERVICE_PRIVATE = "SERVICE_PRIVATE"
    BUSINESS = "BUSINESS"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    FARMER = "FARMER"
    HOUSE_WIFE = "HOUSE_WIFE"
    STUDENT = "STUDENT"
    RETIRED = "RETIRED"
    DOCTOR = "DOCTOR"
    ENGINEER = "ENGINEER"
    TEACHER = "TEACHER"
    LAWYER = "LAWYER"
    ACCOUNTANT = "ACCOUNTANT"
    IT_PROFESSIONAL = "IT_PROFESSIONAL"
    BANKER = "BANKER"
    UNEMPLOYED = "UNEMPLOYED"
    OTHER = "OTHER"


class CardType(PyEnum):
    CLASSIC = "CLASSIC"
    GOLD = "GOLD"
    TITANIUM = "TITANIUM"
    PLATINUM = "PLATINUM"
    SIGNATURE = "SIGNATURE"
    INFINITE = "INFINITE"


class CardNetwork(PyEnum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"


class ResidentialStatus(PyEnum):
    HOUSE_OWNED = "HOUSE_OWNED"
    RENTAL = "RENTAL"
    FAMILY = "FAMILY"
    OTHER = "OTHER"


class AccountApplication(SQLModel, table=True):
    """Account Application Form Schema"""
    id: Optional[int] = Field(default=None, primary_key=True)
    account_no: Optional[str] = None
    date: Optional[str] = None
    iban: Optional[str] = None
    branch_city: Optional[str] = None
    branch_code: Optional[str] = None
    sbp_code: Optional[str] = None
    account_type: Optional[str] = None  # Stored as string: CURRENT, SAVINGS, AHU_LAT
    title_of_account: str  # Required, in block letters
    name_on_card: Optional[str] = None

    # Personal Information
    name: str  # As per CNIC, in block letters
    fathers_husbands_name: Optional[str] = None
    mothers_name: Optional[str] = None
    marital_status: Optional[str] = None  # Stored as string: SINGLE, MARRIED, DIVORCED, WIDOWED
    gender: Optional[str] = None  # Stored as string: MALE, FEMALE, OTHER
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
    occupation: Optional[str] = None  # Stored as string: SERVICE_GOVT, SERVICE_PRIVATE, FARMER, HOUSE_WIFE, STUDENT, OTHER
    occupation_other: Optional[str] = None  # For OTHER occupation

    # Financial Info
    purpose_of_account: Optional[str] = None
    source_of_income: Optional[str] = None
    expected_monthly_turnover_dr: Optional[float] = None  # In Rs (M)
    expected_monthly_turnover_cr: Optional[float] = None  # In Rs (M)

    # Residential Status
    residential_status: Optional[str] = None  # Stored as string: HOUSE_OWNED, RENTAL, FAMILY, OTHER
    residential_status_other: Optional[str] = None  # For OTHER
    residing_since: Optional[str] = None  # Could be date or string

    # Next of Kin - Optional section
    has_next_of_kin: bool = Field(default=False)  # Flag to indicate if kin info is provided
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

    # Card Selection - User chooses ONE card type and network
    card_type: Optional[str] = None  # CLASSIC, GOLD, TITANIUM, PLATINUM, SIGNATURE, INFINITE
    card_network: Optional[str] = None  # VISA or MASTERCARD

    # Zakat Deduction
    zakat_deduction: bool = Field(default=False)

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

    @field_validator('date', 'date_of_birth', 'cnic_expiry_date')
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
    def validate_next_of_kin_info(self) -> 'AccountApplication':
        """Validate that if has_next_of_kin is True, essential fields are required"""
        if self.has_next_of_kin:
            # If kin info is requested, require essential fields
            if not self.next_of_kin_name:
                raise ValueError("Next of kin name is required when has_next_of_kin is True")
            if not self.next_of_kin_relation:
                raise ValueError("Next of kin relation is required when has_next_of_kin is True")
            if not self.next_of_kin_cnic:
                raise ValueError("Next of kin CNIC is required when has_next_of_kin is True")

        return self

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