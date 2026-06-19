from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    amount = Column(Float)

    tax = Column(Float)

    discount = Column(Float)

    total_amount = Column(Float)

    due_date = Column(Date)

    status = Column(
        String,
        default="Pending"
    )

    customer = relationship(
        "Customer",
        back_populates="invoices"
    )

    items = relationship(
        "InvoiceItem",
        back_populates="invoice"
    )
