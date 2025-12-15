from sqlmodel import Session
from fastapi import HTTPException
from model import AccountApplicationCreate, AccountType
from db.schemas import AccountApplication
from typing import List, Optional
from utils.validations import generate_account_number, generate_iban


def create_account_application(application_create: AccountApplicationCreate, session: Session) -> AccountApplication:
    """Create a new account application using model SQL query"""
    try:
        # Convert to full AccountApplication model
        application_data = AccountApplication(**application_create.model_dump())

        # Generate account number and IBAN
        application_data.account_no = generate_account_number()
        application_data.iban = generate_iban()

        return AccountApplication.create(session, application_data)
    except Exception as e:
        print(f"Error creating application: {e}")
        import traceback
        traceback.print_exc()
        raise


def get_account_applications(session: Session) -> List[AccountApplication]:
    """Retrieve all account applications using model SQL query"""
    return AccountApplication.get_all(session)


def get_account_application_by_id(application_id: int, session: Session) -> AccountApplication:
    """Retrieve a specific account application by ID using model SQL query"""
    application = AccountApplication.get_by_id(session, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Account application not found")
    return application


def update_account_application(application_id: int, updated_application: AccountApplication, session: Session) -> AccountApplication:
    """Update an existing account application using model SQL query"""
    update_data = updated_application.model_dump(exclude_unset=True, exclude={'id'})
    application = AccountApplication.update_by_id(session, application_id, update_data)
    if not application:
        raise HTTPException(status_code=404, detail="Account application not found")
    return application


def delete_account_application(application_id: int, session: Session) -> dict:
    """Delete an account application by ID using model SQL query"""
    success = AccountApplication.delete_by_id(session, application_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account application not found")
    return {"message": "Account application deleted successfully"}


# Additional business logic methods using model SQL queries
def get_application_by_cnic(cnic_no: str, session: Session) -> Optional[AccountApplication]:
    """Get account application by CNIC number"""
    return AccountApplication.get_by_cnic(session, cnic_no)


def get_applications_by_account_type(account_type: str, session: Session) -> List[AccountApplication]:
    """Get account applications by account type"""
    try:
        acc_type = AccountType(account_type.upper())
        return AccountApplication.get_by_account_type(session, acc_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid account type")


def get_applications_by_city(city: str, session: Session) -> List[AccountApplication]:
    """Get account applications by city"""
    return AccountApplication.get_by_city(session, city.upper())


def get_total_applications_count(session: Session) -> int:
    """Get total count of account applications"""
    return AccountApplication.count_total(session)


def get_paginated_applications(skip: int = 0, limit: int = 10, session: Session = None) -> List[AccountApplication]:
    """Get paginated account applications"""
    return AccountApplication.get_paginated(session, skip, limit)


def get_application_by_account_number(account_no: str, session: Session) -> Optional[AccountApplication]:
    """Get account application by account number"""
    return AccountApplication.get_by_account_number(session, account_no)


def get_application_by_iban(iban: str, session: Session) -> Optional[AccountApplication]:
    """Get account application by IBAN"""
    return AccountApplication.get_by_iban(session, iban)