from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Product, Purchase, PurchaseItem
from typing import List


async def get_product_by_product_id(db: AsyncSession, product_id: str):
    q = await db.execute(select(Product).where(Product.product_id == product_id))
    return q.scalar_one_or_none()


async def list_products(db: AsyncSession):
    q = await db.execute(select(Product))
    return q.scalars().all()


async def create_purchase(db: AsyncSession, customer_email: str, items: List[dict], total_amount: float,
                          paid_amount: float):
    purchase = Purchase(customer_email=customer_email, total_amount=total_amount, paid_amount=paid_amount)
    db.add(purchase)
    await db.flush()
    # Add items and decrement stock
    for it in items:
        product = await get_product_by_product_id(db, it["product_id"])
        db.add(PurchaseItem(
            purchase_id=purchase.id,
            product_id=it["product_id"],
            quantity=it["quantity"],
            unit_price=product.price_per_unit,
            tax_percentage=product.tax_percentage
        ))
        # update stock
        product.available_stocks = product.available_stocks - it["quantity"]
        db.add(product)
    await db.commit()
    await db.refresh(purchase)
    return purchase


async def list_purchases_for_customer(db: AsyncSession, customer_email: str):
    q = await db.execute(
        select(Purchase).where(Purchase.customer_email == customer_email).order_by(Purchase.created_at.desc()))
    return q.scalars().all()


async def get_purchase(db: AsyncSession, purchase_id: int):
    q = await db.execute(
        select(Purchase)
        .options(
            selectinload(Purchase.items).selectinload(PurchaseItem.product)
        )
        .where(Purchase.id == purchase_id)
    )
    return q.scalar_one_or_none()
