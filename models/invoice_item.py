from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id")
    )

    product_name = Column(String)

    quantity = Column(Integer)

    price = Column(Float)

    invoice = relationship(
        "Invoice",
        back_populates="items"
    )
