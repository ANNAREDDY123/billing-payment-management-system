from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from datetime import date

from database import SessionLocal

from models.customer import Customer
from models.invoice import Invoice
from models.invoice_item import InvoiceItem

from schemas.invoice import InvoiceCreate

from services.invoice_service import (
    calculate_invoice_total
)

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == invoice.customer_id
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

    if invoice.due_date <= date.today():

        raise HTTPException(
            status_code=400,
            detail="Due date must be future date"
        )

    total_amount = calculate_invoice_total(
        invoice.items,
        invoice.tax,
        invoice.discount
    )

    new_invoice = Invoice(
        customer_id=invoice.customer_id,
        amount=total_amount,
        tax=invoice.tax,
        discount=invoice.discount,
        total_amount=total_amount,
        due_date=invoice.due_date,
        status="Pending"
    )

    db.add(new_invoice)

    db.commit()

    db.refresh(new_invoice)

    for item in invoice.items:

        db_item = InvoiceItem(
            invoice_id=new_invoice.id,
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price
        )

        db.add(db_item)

    db.commit()

    return {
        "message":
        "Invoice created successfully",
        "invoice_id":
        new_invoice.id,
        "total_amount":
        total_amount
    }


@router.get("/{invoice_id}")
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):

    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:

        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return invoice


@router.get("/")
def get_invoices(
    status: str = None,
    due_date_before: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Invoice)

    if status:

        query = query.filter(
            Invoice.status == status
        )

    total_records = query.count()

    total_pages = (
        total_records + limit - 1
    ) // limit

    invoices = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records":
        total_records,
        "current_page":
        page,
        "limit":
        limit,
        "total_pages":
        total_pages,
        "data":
        invoices
    }
