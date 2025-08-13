from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# ---------- CREATE MODELS ----------
class PurchaseItemCreate(BaseModel):
    product_id: str
    quantity: int


class PurchaseCreate(BaseModel):
    customer_email: EmailStr
    items: List[PurchaseItemCreate]
    paid_amount: float


# ---------- RESPONSE MODELS ----------
class ProductOut(BaseModel):
    product_id: str
    name: str
    price_per_unit: float
    tax_percentage: float

    class Config:
        orm_mode = True


class PurchaseItemOut(BaseModel):
    id: int
    product_id: str
    quantity: int
    unit_price: float
    tax_percentage: float
    product: Optional[ProductOut]  # Nested product details if needed

    class Config:
        orm_mode = True


class PurchaseOut(BaseModel):
    id: int
    customer_email: EmailStr
    total_amount: float
    paid_amount: float
    created_at: datetime
    items: List[PurchaseItemOut]

    class Config:
        orm_mode = True
