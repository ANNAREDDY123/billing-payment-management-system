from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import (
    Base,
    engine
)

from models.user import User
from models.customer import Customer
from models.invoice import Invoice
from models.invoice_item import InvoiceItem
from models.payment import Payment

from routes.auth import router as auth_router
from routes.customers import router as customer_router
from routes.invoices import router as invoice_router
from routes.payments import router as payment_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Billing & Payment Management System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(invoice_router)
app.include_router(payment_router)


@app.get("/")
def home():

    return {
        "message":
        "Billing & Payment Management System"
    }
