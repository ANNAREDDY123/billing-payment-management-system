from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    BackgroundTasks
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.invoice import Invoice
from models.payment import Payment

from schemas.payment import PaymentCreate

from services.payment_service import (
    validate_payment
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def send_payment_email():

    print(
        "Payment Success Email Sent"
    )


@router.post("/pay/{invoice_id}")
def pay_invoice(
    invoice_id: int,
    payment: PaymentCreate,
    background_tasks: BackgroundTasks,
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

    existing_payment = db.query(Payment).filter(
        Payment.invoice_id == invoice_id
    ).first()

    if existing_payment:

        raise HTTPException(
            status_code=400,
            detail="Invoice already paid"
        )

    if payment.payment_method not in [
        "UPI",
        "Card",
        "Wallet"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Invalid payment method"
        )

    validate_payment(
        invoice.total_amount,
        payment.amount
    )

    new_payment = Payment(
        invoice_id=invoice_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status="Success"
    )

    db.add(new_payment)

    invoice.status = "Paid"

    db.commit()

    db.refresh(new_payment)

    background_tasks.add_task(
        send_payment_email
    )

    return {
        "message":
        "Payment successful",
        "payment_id":
        new_payment.id
    }


@router.get("/{payment_id}")
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):

    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:

        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment
