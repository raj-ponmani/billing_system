from typing import List

from fastapi import HTTPException

from app import crud
from app.utils.denomination import calculate_change_distribution


async def calculate_price(
        paid_amount: float,
        product_id: List[str],
        quantity: List[int], db
):
    items_for_db = []
    items_for_display = []
    total_without_tax = 0.0
    total_tax = 0.0

    for pid, qty in zip(product_id, quantity):
        prod = await crud.get_product_by_product_id(db, pid)
        if not prod:
            raise HTTPException(status_code=404, detail=f"Product {pid} not found")
        if qty <= 0:
            raise HTTPException(status_code=400, detail=f"Invalid quantity for {pid}")

        unit = float(prod.price_per_unit)
        tax_pct = float(prod.tax_percentage)

        purchase_price = unit * qty
        tax_amount = purchase_price * (tax_pct / 100.0)
        total_item_price = purchase_price + tax_amount

        total_without_tax += purchase_price
        total_tax += tax_amount

        items_for_db.append({"product_id": pid, "quantity": qty})
        items_for_display.append({
            "product_id": pid,
            "name": prod.name,
            "quantity": qty,
            "unit_price": unit,
            "purchase_price": round(purchase_price, 2),
            "tax_percentage": tax_pct,
            "tax_amount": round(tax_amount, 2),
            "total_price": round(total_item_price, 2)
        })

    net_price = round(total_without_tax + total_tax, 2)
    rounded_net_price = int(net_price)
    balance_payable = round(paid_amount - rounded_net_price, 2)
    denominations = calculate_change_distribution(balance_payable if balance_payable > 0 else 0)

    return {
        "items": items_for_display,
        "items_for_db": items_for_db,
        "total": net_price,
        "paid": paid_amount,
        "total_without_tax": round(total_without_tax, 2),
        "total_tax": round(total_tax, 2),
        "net_price": net_price,
        "rounded_net_price": rounded_net_price,
        "balance_payable": balance_payable,
        "denominations": denominations
    }