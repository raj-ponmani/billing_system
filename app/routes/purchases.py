from asyncio.log import logger
from pathlib import Path

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.responses import JSONResponse

from app.database import get_db
from app import crud
from app.models import Purchase, PurchaseItem
from app.utils.calculate_price import calculate_price
from app.utils.email_sender import send_invoice_email_async

templates_path = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))
router = APIRouter(prefix="/purchases")


@router.get("/", response_class=HTMLResponse)
async def purchases_index(request: Request, email: str = None, db: AsyncSession = Depends(get_db)):
    """
    If email is provided, list purchases for that customer.
    Otherwise, render a search form.
    """
    purchases = []
    if email:
        purchases = await crud.list_purchases_for_customer(db, email)
    return templates.TemplateResponse("bill_result.html", {"request": request, "purchases": purchases, "email": email})


@router.get("/{purchase_id}", response_class=HTMLResponse)
async def purchase_detail(request: Request, purchase_id: int, db: AsyncSession = Depends(get_db)):
    p = await crud.get_purchase(db, purchase_id)
    if not p:
        raise HTTPException(status_code=404, detail="Purchase not found")

    product_id = [item.product_id for item in p.items]
    quantity = [item.quantity for item in p.items]

    context = await calculate_price(p.paid_amount, product_id, quantity, db)
    context["request"] = request
    context["purchase"] = await crud.get_purchase(db, purchase_id)

    return templates.TemplateResponse("purchase_detail.html", context=context)


@router.get("/send-invoice/{purchase_id}")
async def send_invoice(purchase_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Purchase)
            .options(
                selectinload(Purchase.items).selectinload(PurchaseItem.product)
            )
            .where(Purchase.id == purchase_id)
        )
        purchase = result.scalar_one_or_none()

        if not purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")

        # Prepare items for invoice template
        items_list = []
        for pi in purchase.items:
            amount = pi.unit_price * pi.quantity * (1 + pi.tax_percentage / 100)
            items_list.append({
                "product_id": pi.product.product_id,
                "name": pi.product.name,
                "quantity": pi.quantity,
                "unit_price": pi.unit_price,
                "tax_percentage": pi.tax_percentage,
                "amount": round(amount, 2)
            })

        await send_invoice_email_async(
            email=purchase.customer_email,
            items=items_list,
            total=purchase.total_amount,
            paid=purchase.paid_amount,
            change=round(purchase.paid_amount - purchase.total_amount, 2)
        )

        return JSONResponse(content={"message": f"Invoice email sent to {purchase.customer_email}."})

    except Exception as e:
        logger.exception(f"Error sending invoice for purchase {purchase_id}")
        raise HTTPException(status_code=500, detail=f"Error sending invoice: {str(e)}")
