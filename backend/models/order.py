from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class DeliveryAddress(str, Enum):
    BH1 = "BH1"
    BH2 = "BH2"
    BH3 = "BH3"
    GH1 = "GH1"


# ==================== USER MODELS ====================

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=6, max_length=100)


class UserLogin(BaseModel):
    phone: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=6, max_length=100)


class UserResponse(BaseModel):
    id: str
    name: str
    phone: str
    created_at: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ==================== ORDER ITEM MODELS ====================

class OrderItem(BaseModel):
    name: str
    quantity: int = Field(gt=0)
    price: int


class OrderItemResponse(BaseModel):
    name: str
    quantity: int
    price: int


# ==================== ORDER MODELS ====================

class CreateOrderRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    address: DeliveryAddress
    phone: str = Field(min_length=5, max_length=20)
    items: List[OrderItem] = Field(min_length=1)
    transaction_id: str = Field(min_length=1, max_length=100)
    user_id: Optional[str] = None  # Optional for guest users


class CreateOrderResponse(BaseModel):
    order_id: str
    name: str
    address: DeliveryAddress
    phone: str
    items: List[OrderItemResponse]
    subtotal: int
    delivery_charge: int
    total_price: int
    otp: str
    message: str
    status: str = "pending"
    transaction_id: str


class OrderListResponse(BaseModel):
    orders: List[CreateOrderResponse]
    total: int


# ==================== HEALTH CHECK ====================

class HealthResponse(BaseModel):
    status: str
    service: str
    database: str = "connected"