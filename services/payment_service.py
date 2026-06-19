def validate_payment(
    invoice_amount,
    payment_amount
):

    if invoice_amount != payment_amount:

        raise ValueError(
            "Payment amount must match invoice amount"
        )

    return True
