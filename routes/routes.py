from fastapi import APIRouter, Depends, HTTPException
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
    get_application_by_iban
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


@router.get("/account-applications/count")
def get_applications_count(session: Session = Depends(get_session)):
    """Get total count of account applications"""
    count = get_total_applications_count(session)
    return {"total_applications": count}


@router.get("/account-applications/paginated", response_model=list[AccountApplication])
def get_paginated(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    """Get paginated account applications"""
    return get_paginated_applications(skip, limit, session)


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


