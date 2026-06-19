# billing-payment-management-system
FastAPI Billing &amp; Payment Management System with Customer, Invoice, Payment Processing, JWT Authentication, SQLAlchemy ORM, Pagination, Filtering, Background Tasks, Docker Support, and Clean Architecture.
# Billing & Payment Management System

## Features

- JWT Authentication
- Customer Management
- Invoice Management
- Invoice Items
- Payment Processing
- Filtering
- Pagination
- SQLAlchemy ORM
- SQLite Database
- Background Tasks
- Docker Support

## APIs

### Authentication

- POST /auth/register
- POST /auth/login

### Customers

- POST /customers
- GET /customers/{customer_id}/invoices

### Invoices

- POST /invoices
- GET /invoices/{invoice_id}
- GET /invoices

### Payments

- POST /payments/pay/{invoice_id}
- GET /payments/{payment_id}

## Run

uvicorn main:app --reload
