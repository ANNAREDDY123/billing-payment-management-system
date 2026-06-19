from pydantic import (
    BaseModel,
    Field
)


class PaymentCreate(BaseModel):

    amount: float = Field(gt=0)

    payment_method: str


class PaymentResponse(BaseModel):

    id: int

    invoice_id: int

    amount: float

    payment_method: str

    status: str

    class Config:
        from_attributes = True
