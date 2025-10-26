from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db.connection import get_session
from db.schemas import Item

router = APIRouter()


@router.get("/")
def read_root():
    """Hello World endpoint"""
    return {
        "message": "Hello World!",
        "status": "API is running",
        "version": "1.0.0"
    }


