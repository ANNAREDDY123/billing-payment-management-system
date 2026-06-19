from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.customer import Customer
from models.invoice import Invoice

from schemas.customer import CustomerCreate

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Customer already exists"
        )

    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone
    )

    db.add(new_customer)

    db.commit()

    db.refresh(new_customer)

    return new_customer


@router.get("/{customer_id}/invoices")
def get_customer_invoices(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if not customer.is_active:

        raise HTTPException(
            status_code=400,
            detail="Customer is inactive"
        )

    invoices = db.query(Invoice).filter(
        Invoice.customer_id == customer_id
    ).all()

    return invoices
