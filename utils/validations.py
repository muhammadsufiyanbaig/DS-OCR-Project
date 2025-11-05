import re
import random
import string
from typing import Optional


def validate_uppercase(v: Optional[str]) -> Optional[str]:
    """Validate that the field is in BLOCK LETTERS (uppercase only)"""
    if v is not None and not v.isupper():
        raise ValueError('This field must be in BLOCK LETTERS (uppercase only)')
    return v


def validate_cnic(v: str) -> str:
    """Validate CNIC format: XXXXX-XXXXXXX-X"""
    if not re.match(r'^\d{5}-\d{7}-\d{1}$', v):
        raise ValueError('CNIC must be in format XXXXX-XXXXXXX-X (e.g., 12345-1234567-1)')
    return v


def validate_kin_cnic(v: Optional[str]) -> Optional[str]:
    """Validate Next of Kin CNIC format"""
    if v is not None and not re.match(r'^\d{5}-\d{7}-\d{1}$', v):
        raise ValueError('Next of Kin CNIC must be in format XXXXX-XXXXXXX-X')
    return v


def validate_date_format(v: Optional[str]) -> Optional[str]:
    """Validate date format: DD MM YY"""
    if v is not None and not re.match(r'^\d{2} \d{2} \d{2}$', v):
        raise ValueError('Date must be in format DD MM YY (e.g., 01 01 25)')
    return v


def validate_postal_code(v: Optional[str]) -> Optional[str]:
    """Validate postal code contains only digits"""
    if v is not None and not re.match(r'^\d+$', v):
        raise ValueError('Postal code must contain only digits')
    return v


def validate_contact(v: Optional[str]) -> Optional[str]:
    """Validate contact number contains only digits"""
    if v is not None and not re.match(r'^\d+$', v):
        raise ValueError('Contact number must contain only digits')
    return v


def validate_email(v: Optional[str]) -> Optional[str]:
    """Validate email format"""
    if v is not None and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', v):
        raise ValueError('Invalid email format')
    return v


def generate_account_number() -> str:
    """Generate a random 12-digit account number"""
    return ''.join(random.choices(string.digits, k=12))


def generate_iban() -> str:
    """Generate a random Pakistani IBAN (PK + 2 check digits + 16 digits)"""
    # Pakistani IBAN format: PK + 2 check digits + 16 digits
    check_digits = ''.join(random.choices(string.digits, k=2))
    account_digits = ''.join(random.choices(string.digits, k=16))
    return f"PK{check_digits}{account_digits}"


def validate_account_number(v: Optional[str]) -> Optional[str]:
    """Validate account number format (12 digits)"""
    if v is not None and not re.match(r'^\d{12}$', v):
        raise ValueError('Account number must be 12 digits')
    return v


def validate_iban(v: Optional[str]) -> Optional[str]:
    """Validate IBAN format (PK followed by 18 digits)"""
    if v is not None and not re.match(r'^PK\d{18}$', v):
        raise ValueError('IBAN must be in format PK followed by 18 digits')
    return v