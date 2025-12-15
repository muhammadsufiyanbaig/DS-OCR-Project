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

    # Analytics Query Methods
    @classmethod
    def count_by_account_type(cls, session: Session) -> dict:
        """Get count of applications grouped by account type"""
        from sqlmodel import func
        results = session.exec(
            select(cls.account_type, func.count(cls.id))
            .group_by(cls.account_type)
        ).all()
        return {acc_type or "UNKNOWN": count for acc_type, count in results}

    @classmethod
    def count_by_city(cls, session: Session) -> dict:
        """Get count of applications grouped by city"""
        from sqlmodel import func
        results = session.exec(
            select(cls.city, func.count(cls.id))
            .group_by(cls.city)
        ).all()
        return {city or "UNKNOWN": count for city, count in results}

    @classmethod
    def count_by_gender(cls, session: Session) -> dict:
        """Get count of applications grouped by gender"""
        from sqlmodel import func
        results = session.exec(
            select(cls.gender, func.count(cls.id))
            .group_by(cls.gender)
        ).all()
        return {gender or "UNKNOWN": count for gender, count in results}

    @classmethod
    def count_by_occupation(cls, session: Session) -> dict:
        """Get count of applications grouped by occupation"""
        from sqlmodel import func
        results = session.exec(
            select(cls.occupation, func.count(cls.id))
            .group_by(cls.occupation)
        ).all()
        return {occupation or "UNKNOWN": count for occupation, count in results}

    @classmethod
    def count_by_card_type(cls, session: Session) -> dict:
        """Get count of applications grouped by card type"""
        from sqlmodel import func
        results = session.exec(
            select(cls.card_type, func.count(cls.id))
            .group_by(cls.card_type)
        ).all()
        return {card_type or "NO_CARD": count for card_type, count in results}

    @classmethod
    def count_by_card_network(cls, session: Session) -> dict:
        """Get count of applications grouped by card network"""
        from sqlmodel import func
        results = session.exec(
            select(cls.card_network, func.count(cls.id))
            .group_by(cls.card_network)
        ).all()
        return {network or "NO_CARD": count for network, count in results}

    @classmethod
    def count_by_marital_status(cls, session: Session) -> dict:
        """Get count of applications grouped by marital status"""
        from sqlmodel import func
        results = session.exec(
            select(cls.marital_status, func.count(cls.id))
            .group_by(cls.marital_status)
        ).all()
        return {status or "UNKNOWN": count for status, count in results}

    @classmethod
    def count_by_residential_status(cls, session: Session) -> dict:
        """Get count of applications grouped by residential status"""
        from sqlmodel import func
        results = session.exec(
            select(cls.residential_status, func.count(cls.id))
            .group_by(cls.residential_status)
        ).all()
        return {status or "UNKNOWN": count for status, count in results}

    @classmethod
    def get_services_stats(cls, session: Session) -> dict:
        """Get count of applications with each service enabled"""
        from sqlmodel import func
        
        internet_banking = session.exec(
            select(func.count(cls.id)).where(cls.internet_banking == True)
        ).one()
        mobile_banking = session.exec(
            select(func.count(cls.id)).where(cls.mobile_banking == True)
        ).one()
        check_book = session.exec(
            select(func.count(cls.id)).where(cls.check_book == True)
        ).one()
        sms_alerts = session.exec(
            select(func.count(cls.id)).where(cls.sms_alerts == True)
        ).one()
        zakat_deduction = session.exec(
            select(func.count(cls.id)).where(cls.zakat_deduction == True)
        ).one()
        
        return {
            "internet_banking": internet_banking,
            "mobile_banking": mobile_banking,
            "check_book": check_book,
            "sms_alerts": sms_alerts,
            "zakat_deduction": zakat_deduction
        }

    @classmethod
    def get_kin_stats(cls, session: Session) -> dict:
        """Get count of applications with/without next of kin"""
        from sqlmodel import func
        
        with_kin = session.exec(
            select(func.count(cls.id)).where(cls.has_next_of_kin == True)
        ).one()
        without_kin = session.exec(
            select(func.count(cls.id)).where(cls.has_next_of_kin == False)
        ).one()
        
        return {
            "with_next_of_kin": with_kin,
            "without_next_of_kin": without_kin
        }

    # ==================== ADVANCED ANALYTICS ====================
    
    @classmethod
    def get_all_applications_raw(cls, session: Session) -> List['AccountApplication']:
        """Get all applications for complex analytics processing"""
        return session.exec(select(cls)).all()

    @classmethod
    def get_financial_stats(cls, session: Session) -> dict:
        """Get financial statistics - avg, min, max turnover"""
        from sqlmodel import func
        
        # Debit turnover stats
        dr_stats = session.exec(
            select(
                func.avg(cls.expected_monthly_turnover_dr),
                func.min(cls.expected_monthly_turnover_dr),
                func.max(cls.expected_monthly_turnover_dr),
                func.sum(cls.expected_monthly_turnover_dr)
            ).where(cls.expected_monthly_turnover_dr != None)
        ).first()
        
        # Credit turnover stats
        cr_stats = session.exec(
            select(
                func.avg(cls.expected_monthly_turnover_cr),
                func.min(cls.expected_monthly_turnover_cr),
                func.max(cls.expected_monthly_turnover_cr),
                func.sum(cls.expected_monthly_turnover_cr)
            ).where(cls.expected_monthly_turnover_cr != None)
        ).first()
        
        return {
            "debit_turnover": {
                "average": float(dr_stats[0]) if dr_stats[0] else 0,
                "minimum": float(dr_stats[1]) if dr_stats[1] else 0,
                "maximum": float(dr_stats[2]) if dr_stats[2] else 0,
                "total": float(dr_stats[3]) if dr_stats[3] else 0
            },
            "credit_turnover": {
                "average": float(cr_stats[0]) if cr_stats[0] else 0,
                "minimum": float(cr_stats[1]) if cr_stats[1] else 0,
                "maximum": float(cr_stats[2]) if cr_stats[2] else 0,
                "total": float(cr_stats[3]) if cr_stats[3] else 0
            }
        }

    @classmethod
    def get_cross_analysis_gender_account(cls, session: Session) -> dict:
        """Cross-tabulation: Gender vs Account Type"""
        from sqlmodel import func
        results = session.exec(
            select(cls.gender, cls.account_type, func.count(cls.id))
            .group_by(cls.gender, cls.account_type)
        ).all()
        
        cross_data = {}
        for gender, acc_type, count in results:
            gender_key = gender or "UNKNOWN"
            if gender_key not in cross_data:
                cross_data[gender_key] = {}
            cross_data[gender_key][acc_type or "UNKNOWN"] = count
        
        return cross_data

    @classmethod
    def get_cross_analysis_occupation_card(cls, session: Session) -> dict:
        """Cross-tabulation: Occupation vs Card Type"""
        from sqlmodel import func
        results = session.exec(
            select(cls.occupation, cls.card_type, func.count(cls.id))
            .group_by(cls.occupation, cls.card_type)
        ).all()
        
        cross_data = {}
        for occupation, card_type, count in results:
            occ_key = occupation or "UNKNOWN"
            if occ_key not in cross_data:
                cross_data[occ_key] = {}
            cross_data[occ_key][card_type or "NO_CARD"] = count
        
        return cross_data

    @classmethod
    def get_city_performance(cls, session: Session) -> List[dict]:
        """Get comprehensive city-wise performance metrics"""
        from sqlmodel import func
        
        results = session.exec(
            select(
                cls.city,
                func.count(cls.id),
                func.avg(cls.expected_monthly_turnover_cr),
                func.sum(cls.expected_monthly_turnover_cr)
            )
            .group_by(cls.city)
            .order_by(func.count(cls.id).desc())
        ).all()
        
        return [
            {
                "city": city or "UNKNOWN",
                "total_applications": count,
                "avg_monthly_credit": round(float(avg_cr), 2) if avg_cr else 0,
                "total_monthly_credit": round(float(sum_cr), 2) if sum_cr else 0
            }
            for city, count, avg_cr, sum_cr in results
        ]

    @classmethod
    def get_avg_turnover_by_occupation(cls, session: Session) -> List[dict]:
        """Get average turnover grouped by occupation"""
        from sqlmodel import func
        
        results = session.exec(
            select(
                cls.occupation,
                func.count(cls.id),
                func.avg(cls.expected_monthly_turnover_dr),
                func.avg(cls.expected_monthly_turnover_cr)
            )
            .group_by(cls.occupation)
            .order_by(func.avg(cls.expected_monthly_turnover_cr).desc())
        ).all()
        
        return [
            {
                "occupation": occ or "UNKNOWN",
                "count": count,
                "avg_debit": round(float(avg_dr), 2) if avg_dr else 0,
                "avg_credit": round(float(avg_cr), 2) if avg_cr else 0
            }
            for occ, count, avg_dr, avg_cr in results
        ]

    @classmethod
    def get_premium_card_demographics(cls, session: Session) -> dict:
        """Analyze demographics of premium card holders (PLATINUM, SIGNATURE, INFINITE)"""
        from sqlmodel import func
        
        premium_cards = ['PLATINUM', 'SIGNATURE', 'INFINITE']
        
        # Gender distribution
        gender_dist = session.exec(
            select(cls.gender, func.count(cls.id))
            .where(cls.card_type.in_(premium_cards))
            .group_by(cls.gender)
        ).all()
        
        # Occupation distribution
        occupation_dist = session.exec(
            select(cls.occupation, func.count(cls.id))
            .where(cls.card_type.in_(premium_cards))
            .group_by(cls.occupation)
        ).all()
        
        # City distribution
        city_dist = session.exec(
            select(cls.city, func.count(cls.id))
            .where(cls.card_type.in_(premium_cards))
            .group_by(cls.city)
            .order_by(func.count(cls.id).desc())
            .limit(10)
        ).all()
        
        # Average turnover for premium vs non-premium
        premium_avg = session.exec(
            select(func.avg(cls.expected_monthly_turnover_cr))
            .where(cls.card_type.in_(premium_cards))
        ).first()
        
        non_premium_avg = session.exec(
            select(func.avg(cls.expected_monthly_turnover_cr))
            .where(cls.card_type.not_in(premium_cards))
        ).first()
        
        return {
            "total_premium_holders": sum(count for _, count in gender_dist),
            "gender_distribution": {g or "UNKNOWN": c for g, c in gender_dist},
            "occupation_distribution": {o or "UNKNOWN": c for o, c in occupation_dist},
            "top_cities": {city or "UNKNOWN": c for city, c in city_dist},
            "avg_monthly_credit_premium": round(float(premium_avg[0]), 2) if premium_avg and premium_avg[0] else 0,
            "avg_monthly_credit_non_premium": round(float(non_premium_avg[0]), 2) if non_premium_avg and non_premium_avg[0] else 0
        }

    @classmethod
    def get_digital_adoption_analysis(cls, session: Session) -> dict:
        """Analyze digital services adoption patterns"""
        from sqlmodel import func
        
        total = session.exec(select(func.count(cls.id))).one()
        
        # Both internet and mobile banking
        full_digital = session.exec(
            select(func.count(cls.id))
            .where(cls.internet_banking == True)
            .where(cls.mobile_banking == True)
        ).one()
        
        # Only internet banking
        internet_only = session.exec(
            select(func.count(cls.id))
            .where(cls.internet_banking == True)
            .where(cls.mobile_banking == False)
        ).one()
        
        # Only mobile banking
        mobile_only = session.exec(
            select(func.count(cls.id))
            .where(cls.internet_banking == False)
            .where(cls.mobile_banking == True)
        ).one()
        
        # No digital banking
        no_digital = session.exec(
            select(func.count(cls.id))
            .where(cls.internet_banking == False)
            .where(cls.mobile_banking == False)
        ).one()
        
        # Digital adoption by account type
        digital_by_account = session.exec(
            select(cls.account_type, func.count(cls.id))
            .where((cls.internet_banking == True) | (cls.mobile_banking == True))
            .group_by(cls.account_type)
        ).all()
        
        return {
            "total_customers": total,
            "full_digital_customers": full_digital,
            "internet_only": internet_only,
            "mobile_only": mobile_only,
            "no_digital": no_digital,
            "digital_adoption_rate": round((full_digital / total) * 100, 2) if total > 0 else 0,
            "any_digital_rate": round(((full_digital + internet_only + mobile_only) / total) * 100, 2) if total > 0 else 0,
            "digital_by_account_type": {acc or "UNKNOWN": c for acc, c in digital_by_account}
        }

    @classmethod
    def get_high_value_customers(cls, session: Session, threshold: float = 500000) -> dict:
        """Identify and analyze high-value customers (above threshold monthly credit)"""
        from sqlmodel import func
        
        # High value customers
        high_value = session.exec(
            select(cls)
            .where(cls.expected_monthly_turnover_cr >= threshold)
            .order_by(cls.expected_monthly_turnover_cr.desc())
        ).all()
        
        total_high_value = len(high_value)
        total_all = session.exec(select(func.count(cls.id))).one()
        
        # Analyze high value customer profiles
        card_dist = {}
        occupation_dist = {}
        city_dist = {}
        account_dist = {}
        
        for customer in high_value:
            card_dist[customer.card_type or "NO_CARD"] = card_dist.get(customer.card_type or "NO_CARD", 0) + 1
            occupation_dist[customer.occupation or "UNKNOWN"] = occupation_dist.get(customer.occupation or "UNKNOWN", 0) + 1
            city_dist[customer.city or "UNKNOWN"] = city_dist.get(customer.city or "UNKNOWN", 0) + 1
            account_dist[customer.account_type or "UNKNOWN"] = account_dist.get(customer.account_type or "UNKNOWN", 0) + 1
        
        return {
            "threshold": threshold,
            "total_high_value_customers": total_high_value,
            "percentage_of_total": round((total_high_value / total_all) * 100, 2) if total_all > 0 else 0,
            "preferred_card_types": dict(sorted(card_dist.items(), key=lambda x: x[1], reverse=True)),
            "top_occupations": dict(sorted(occupation_dist.items(), key=lambda x: x[1], reverse=True)[:5]),
            "top_cities": dict(sorted(city_dist.items(), key=lambda x: x[1], reverse=True)[:5]),
            "account_type_preference": account_dist
        }

    @classmethod
    def get_profile_completeness(cls, session: Session) -> dict:
        """Analyze how complete customer profiles are"""
        all_apps = session.exec(select(cls)).all()
        
        completeness_scores = []
        field_completion = {
            "fathers_husbands_name": 0,
            "mothers_name": 0,
            "date_of_birth": 0,
            "nationality": 0,
            "place_of_birth": 0,
            "address_complete": 0,
            "occupation": 0,
            "financial_info": 0,
            "residential_status": 0,
            "next_of_kin": 0,
            "card_selected": 0
        }
        
        for app in all_apps:
            score = 0
            total_fields = 11
            
            if app.fathers_husbands_name:
                score += 1
                field_completion["fathers_husbands_name"] += 1
            if app.mothers_name:
                score += 1
                field_completion["mothers_name"] += 1
            if app.date_of_birth:
                score += 1
                field_completion["date_of_birth"] += 1
            if app.nationality:
                score += 1
                field_completion["nationality"] += 1
            if app.place_of_birth:
                score += 1
                field_completion["place_of_birth"] += 1
            if app.house_no_block_street and app.city and app.postal_code:
                score += 1
                field_completion["address_complete"] += 1
            if app.occupation:
                score += 1
                field_completion["occupation"] += 1
            if app.expected_monthly_turnover_cr or app.expected_monthly_turnover_dr:
                score += 1
                field_completion["financial_info"] += 1
            if app.residential_status:
                score += 1
                field_completion["residential_status"] += 1
            if app.has_next_of_kin and app.next_of_kin_name:
                score += 1
                field_completion["next_of_kin"] += 1
            if app.card_type:
                score += 1
                field_completion["card_selected"] += 1
            
            completeness_scores.append((score / total_fields) * 100)
        
        total_apps = len(all_apps)
        avg_completeness = sum(completeness_scores) / total_apps if total_apps > 0 else 0
        
        return {
            "total_applications": total_apps,
            "average_completeness_percentage": round(avg_completeness, 2),
            "fully_complete_profiles": sum(1 for s in completeness_scores if s == 100),
            "above_80_percent": sum(1 for s in completeness_scores if s >= 80),
            "below_50_percent": sum(1 for s in completeness_scores if s < 50),
            "field_completion_rates": {
                k: round((v / total_apps) * 100, 2) if total_apps > 0 else 0 
                for k, v in field_completion.items()
            }
        }

    @classmethod
    def get_customer_segments(cls, session: Session) -> dict:
        """Segment customers based on multiple factors"""
        all_apps = session.exec(select(cls)).all()
        
        segments = {
            "premium_digital_natives": [],  # Premium cards + full digital
            "high_value_traditional": [],   # High turnover, no digital
            "young_professionals": [],       # Students/service + digital
            "business_owners": [],           # Business occupation
            "value_seekers": [],             # Basic cards, basic services
            "fully_engaged": []              # All services enabled
        }
        
        for app in all_apps:
            # Premium Digital Natives
            if app.card_type in ['PLATINUM', 'SIGNATURE', 'INFINITE'] and app.internet_banking and app.mobile_banking:
                segments["premium_digital_natives"].append(app.id)
            
            # High Value Traditional
            if (app.expected_monthly_turnover_cr and app.expected_monthly_turnover_cr >= 300000 and 
                not app.internet_banking and not app.mobile_banking):
                segments["high_value_traditional"].append(app.id)
            
            # Young Professionals (assuming students and new employees)
            if app.occupation in ['STUDENT', 'SERVICE_PRIVATE', 'IT_PROFESSIONAL'] and (app.internet_banking or app.mobile_banking):
                segments["young_professionals"].append(app.id)
            
            # Business Owners
            if app.occupation in ['BUSINESS', 'SELF_EMPLOYED']:
                segments["business_owners"].append(app.id)
            
            # Value Seekers
            if app.card_type in ['CLASSIC', None] and not app.internet_banking:
                segments["value_seekers"].append(app.id)
            
            # Fully Engaged
            if (app.internet_banking and app.mobile_banking and 
                app.sms_alerts and app.card_type):
                segments["fully_engaged"].append(app.id)
        
        total = len(all_apps)
        return {
            "total_customers": total,
            "segments": {
                k: {
                    "count": len(v),
                    "percentage": round((len(v) / total) * 100, 2) if total > 0 else 0
                }
                for k, v in segments.items()
            }
        }