from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from db.connection import get_session
from model import Item, AccountApplicationCreate
from db.schemas import AccountApplication
from controller.account_application import (
    create_account_application,
    get_account_applications,
    get_account_application_by_id,
    update_account_application,
    delete_account_application,
    get_application_by_cnic,
    get_applications_by_account_type,
    get_applications_by_city,
    get_total_applications_count,
    get_paginated_applications,
    get_application_by_account_number,
    get_application_by_iban,
    # Basic Analytics imports
    get_analytics_by_account_type,
    get_analytics_by_city,
    get_analytics_by_gender,
    get_analytics_by_occupation,
    get_analytics_by_card_type,
    get_analytics_by_card_network,
    get_analytics_by_marital_status,
    get_analytics_by_residential_status,
    get_services_analytics,
    get_kin_analytics,
    get_dashboard_summary,
    # Advanced Analytics imports
    get_financial_insights,
    get_gender_account_cross_analysis,
    get_occupation_card_cross_analysis,
    get_city_performance_analytics,
    get_occupation_income_analysis,
    get_premium_customer_analysis,
    get_digital_banking_insights,
    get_high_value_customer_insights,
    get_profile_completeness_analytics,
    get_customer_segmentation,
    get_executive_summary
)

router = APIRouter()


@router.get("/")
def read_root():
    """Hello World endpoint"""
    return {
        "message": "Hello World!",
        "status": "API is running",
        "version": "1.0.0"
    }


@router.post("/account-applications", response_model=AccountApplication)
def create_application(application_create: AccountApplicationCreate, session: Session = Depends(get_session)):
    """Create a new account application (account_no and iban are auto-generated)
    
    Validation Rules:
    - Account title, name, and card name must be identical
    - Next of Kin: If any kin info provided, name/relation/CNIC are required
    - All text fields must be in BLOCK LETTERS (uppercase)
    """
    return create_account_application(application_create, session)


@router.get("/account-applications", response_model=list[AccountApplication])
def read_applications(session: Session = Depends(get_session)):
    """Read all account applications"""
    return get_account_applications(session)


@router.get("/account-applications/count")
def get_applications_count(session: Session = Depends(get_session)):
    """Get total count of account applications"""
    count = get_total_applications_count(session)
    return {"total_applications": count}


@router.get("/account-applications/paginated", response_model=list[AccountApplication])
def get_paginated(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    """Get paginated account applications"""
    return get_paginated_applications(skip, limit, session)


@router.get("/account-applications/search/cnic/{cnic_no}", response_model=AccountApplication)
def search_by_cnic(cnic_no: str, session: Session = Depends(get_session)):
    """Search account application by CNIC number"""
    application = get_application_by_cnic(cnic_no, session)
    if not application:
        raise HTTPException(status_code=404, detail="Account application not found")
    return application


@router.get("/account-applications/search/account-type/{account_type}", response_model=list[AccountApplication])
def search_by_account_type(account_type: str, session: Session = Depends(get_session)):
    """Search account applications by account type"""
    return get_applications_by_account_type(account_type, session)


@router.get("/account-applications/search/city/{city}", response_model=list[AccountApplication])
def search_by_city(city: str, session: Session = Depends(get_session)):
    """Search account applications by city"""
    return get_applications_by_city(city, session)


@router.get("/account-applications/search/account-number/{account_no}", response_model=AccountApplication)
def search_by_account_number(account_no: str, session: Session = Depends(get_session)):
    """Search account application by account number"""
    application = get_application_by_account_number(account_no, session)
    if not application:
        raise HTTPException(status_code=404, detail="Account application not found")
    return application


@router.get("/account-applications/search/iban/{iban}", response_model=AccountApplication)
def search_by_iban(iban: str, session: Session = Depends(get_session)):
    """Search account application by IBAN"""
    application = get_application_by_iban(iban, session)
    if not application:
        raise HTTPException(status_code=404, detail="Account application not found")
    return application


@router.get("/account-applications/{application_id}", response_model=AccountApplication)
def read_application(application_id: int, session: Session = Depends(get_session)):
    """Read a specific account application by ID"""
    return get_account_application_by_id(application_id, session)


@router.put("/account-applications/{application_id}", response_model=AccountApplication)
def update_application(application_id: int, updated_application: AccountApplication, session: Session = Depends(get_session)):
    """Update an existing account application"""
    return update_account_application(application_id, updated_application, session)


@router.delete("/account-applications/{application_id}")
def delete_application(application_id: int, session: Session = Depends(get_session)):
    """Delete an account application by ID"""
    return delete_account_application(application_id, session)


# ==================== ANALYTICS ENDPOINTS ====================

@router.get("/analytics/dashboard")
def get_dashboard(session: Session = Depends(get_session)):
    """Get comprehensive dashboard summary with all key metrics"""
    return get_dashboard_summary(session)


@router.get("/analytics/account-types")
def analytics_account_types(session: Session = Depends(get_session)):
    """Get analytics breakdown by account type (CURRENT, SAVINGS, AHU_LAT)"""
    return get_analytics_by_account_type(session)


@router.get("/analytics/cities")
def analytics_cities(session: Session = Depends(get_session)):
    """Get analytics breakdown by city"""
    return get_analytics_by_city(session)


@router.get("/analytics/gender")
def analytics_gender(session: Session = Depends(get_session)):
    """Get analytics breakdown by gender (MALE, FEMALE, OTHER)"""
    return get_analytics_by_gender(session)


@router.get("/analytics/occupation")
def analytics_occupation(session: Session = Depends(get_session)):
    """Get analytics breakdown by occupation"""
    return get_analytics_by_occupation(session)


@router.get("/analytics/card-types")
def analytics_card_types(session: Session = Depends(get_session)):
    """Get analytics breakdown by card type (CLASSIC, GOLD, TITANIUM, etc.)"""
    return get_analytics_by_card_type(session)


@router.get("/analytics/card-networks")
def analytics_card_networks(session: Session = Depends(get_session)):
    """Get analytics breakdown by card network (VISA, MASTERCARD)"""
    return get_analytics_by_card_network(session)


@router.get("/analytics/marital-status")
def analytics_marital_status(session: Session = Depends(get_session)):
    """Get analytics breakdown by marital status"""
    return get_analytics_by_marital_status(session)


@router.get("/analytics/residential-status")
def analytics_residential_status(session: Session = Depends(get_session)):
    """Get analytics breakdown by residential status"""
    return get_analytics_by_residential_status(session)


@router.get("/analytics/services")
def analytics_services(session: Session = Depends(get_session)):
    """Get analytics for services adoption (internet banking, mobile banking, etc.)"""
    return get_services_analytics(session)


@router.get("/analytics/next-of-kin")
def analytics_kin(session: Session = Depends(get_session)):
    """Get analytics for next of kin (with/without kin information)"""
    return get_kin_analytics(session)


# ==================== ADVANCED ANALYTICS ENDPOINTS ====================

@router.get("/analytics/executive-summary")
def analytics_executive_summary(session: Session = Depends(get_session)):
    """
    Executive Summary: Comprehensive business intelligence report with key metrics,
    health indicators, and actionable recommendations for decision makers.
    """
    return get_executive_summary(session)


@router.get("/analytics/financial-insights")
def analytics_financial(session: Session = Depends(get_session)):
    """
    Financial Analytics: Detailed analysis of expected monthly turnovers including
    average, min, max values and net cash flow predictions.
    """
    return get_financial_insights(session)


@router.get("/analytics/cross-analysis/gender-account")
def analytics_gender_account(session: Session = Depends(get_session)):
    """
    Cross-Tabulation: Gender vs Account Type analysis showing which account types
    are preferred by different genders with distribution insights.
    """
    return get_gender_account_cross_analysis(session)


@router.get("/analytics/cross-analysis/occupation-card")
def analytics_occupation_card(session: Session = Depends(get_session)):
    """
    Cross-Tabulation: Occupation vs Card Type analysis showing premium card adoption
    rates by occupation and top premium card adopter demographics.
    """
    return get_occupation_card_cross_analysis(session)


@router.get("/analytics/city-performance")
def analytics_city_performance(session: Session = Depends(get_session)):
    """
    City Performance Analysis: Comprehensive city-wise metrics including application volume,
    average customer value, total deposits, and city rankings.
    """
    return get_city_performance_analytics(session)


@router.get("/analytics/occupation-income")
def analytics_occupation_income(session: Session = Depends(get_session)):
    """
    Occupation Income Analysis: Average income patterns by occupation with income tier
    classification (HIGH/MEDIUM/LOW) and earning comparisons.
    """
    return get_occupation_income_analysis(session)


@router.get("/analytics/premium-customers")
def analytics_premium_customers(session: Session = Depends(get_session)):
    """
    Premium Customer Demographics: In-depth analysis of PLATINUM, SIGNATURE, and INFINITE
    card holders including their demographics, income comparison, and profile.
    """
    return get_premium_customer_analysis(session)


@router.get("/analytics/digital-banking")
def analytics_digital_banking(session: Session = Depends(get_session)):
    """
    Digital Banking Adoption: Comprehensive analysis of digital service adoption including
    maturity scoring, adoption rates, and recommendations for improvement.
    """
    return get_digital_banking_insights(session)


@router.get("/analytics/high-value-customers")
def analytics_high_value(
    session: Session = Depends(get_session),
    threshold: float = Query(default=500000, description="Monthly credit threshold for high-value classification")
):
    """
    High-Value Customer Analysis: Identify customers above the specified monthly credit threshold
    with demographics, preferences, and targeting recommendations.
    """
    return get_high_value_customer_insights(session, threshold)


@router.get("/analytics/profile-completeness")
def analytics_profile_completeness(session: Session = Depends(get_session)):
    """
    Profile Completeness Analysis: Measure data quality across customer profiles with
    field-by-field completion rates and improvement recommendations.
    """
    return get_profile_completeness_analytics(session)


@router.get("/analytics/customer-segments")
def analytics_customer_segments(session: Session = Depends(get_session)):
    """
    Customer Segmentation: Behavioral segmentation including Premium Digital Natives,
    High-Value Traditional, Young Professionals, Business Owners, and more with
    targeted recommendations for each segment.
    """
    return get_customer_segmentation(session)


