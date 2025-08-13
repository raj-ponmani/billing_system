from pathlib import Path

from fastapi import APIRouter, Request, Depends, Form, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app import crud
from app.utils.calculate_price import calculate_price
from app.utils.email_sender import send_invoice_email_async

templates_path = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def billing_form(request: Request, db: AsyncSession = Depends(get_db)):
    products = await crud.list_products(db)
    return templates.TemplateResponse("billing_form.html", {"request": request, "products": products})


@router.post("/generate-bill", response_class=HTMLResponse)
async def generate_bill(
        request: Request,
        background_tasks: BackgroundTasks,
        customer_email: str = Form(...),
        paid_amount: float = Form(...),
        product_id: List[str] = Form(...),
        quantity: List[int] = Form(...),
        db: AsyncSession = Depends(get_db)
):
    if len(product_id) != len(quantity):
        raise HTTPException(status_code=400, detail="Product and quantity mismatch")

    context = await calculate_price(paid_amount, product_id, quantity, db)
    purchase = await crud.create_purchase(
        db,
        customer_email,
        context["items_for_db"],
        context["rounded_net_price"],
        paid_amount
    )
    context["purchase"] = purchase

    # Send email in background
    background_tasks.add_task(
        send_invoice_email_async,
        customer_email,
        context["items"],
        context["rounded_net_price"],
        paid_amount,
        context["balance_payable"],
        context["denominations"]
    )
    context["request"] = request

    return templates.TemplateResponse(
        "purchase_detail.html",
        context=context
    )

