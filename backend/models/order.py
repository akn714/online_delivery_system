from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class DeliveryAddress(str, Enum):
    BH1 = "BH1"
    BH2 = "BH2"
    BH3 = "BH3"
    GH1 = "GH1"


class OrderItem(BaseModel):
    name: str
    quantity: int = Field(gt=0)
    price: int


class CreateOrderRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    address: DeliveryAddress
    phone: str = Field(min_length=5, max_length=20)
    items: List[OrderItem] = Field(min_length=1)


class OrderItemResponse(BaseModel):
    name: str
    quantity: int
    price: int


class CreateOrderResponse(BaseModel):
    order_id: str
    name: str
    address: DeliveryAddress
    phone: str
    items: List[OrderItemResponse]
    subtotal: int
    delivery_charge: int
    total_price: int
    message: str