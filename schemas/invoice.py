from pydantic import (
    BaseModel,
    Field
)

from datetime import date


class InvoiceItemCreate(BaseModel):

    product_name: str

    quantity: int = Field(gt=0)

    price: float = Field(gt=0)


class InvoiceCreate(BaseModel):

    customer_id: int

    tax: float = 0

    discount: float = 0

    due_date: date

    items: list[InvoiceItemCreate]
