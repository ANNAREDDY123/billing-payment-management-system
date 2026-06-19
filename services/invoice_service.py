def calculate_invoice_total(
    items,
    tax,
    discount
):

    subtotal = 0

    for item in items:

        subtotal += (
            item.quantity
            * item.price
        )

    total = (
        subtotal
        + tax
        - discount
    )

    if total <= 0:

        raise ValueError(
            "Invalid invoice total"
        )

    return total
