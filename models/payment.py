from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey
)

from database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        unique=True
    )

    amount = Column(Float)

    payment_method = Column(String)

    status = Column(String)
