from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

from models.order import (
    CreateOrderRequest, 
    CreateOrderResponse,
    OrderItemResponse
)
from services.telegram import send_order_to_telegram, format_telegram_message

load_dotenv()

router = APIRouter(prefix="/api", tags=["orders"])

DELIVERY_CHARGE = int(os.getenv("DELIVERY_CHARGE", "15"))


@router.post("/create-order", response_model=CreateOrderResponse)
async def create_order(request: CreateOrderRequest):
    """
    Create a new order and send notification to Telegram.
    """
    # Generate unique order ID
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    order_id = f"Order#{timestamp}-{uuid.uuid4().hex[:4].upper()}"
    
    # Calculate subtotal
    subtotal = sum(item.price * item.quantity for item in request.items)
    
    # Calculate total
    total_price = subtotal + DELIVERY_CHARGE
    
    # Format items for response
    items_response = [
        OrderItemResponse(
            name=item.name,
            quantity=item.quantity,
            price=item.price
        )
        for item in request.items
    ]
    
    # Format items for Telegram
    items_for_telegram = [
        {"name": item.name, "quantity": item.quantity}
        for item in request.items
    ]
    
    # Send to Telegram (async, don't wait for success to return)
    telegram_result = await send_order_to_telegram(
        order_id=order_id,
        name=request.name,
        address=request.address.value,
        phone=request.phone,
        items=items_for_telegram,
        subtotal=subtotal,
        delivery_charge=DELIVERY_CHARGE,
        total_price=total_price
    )
    
    # Format message for response
    message = format_telegram_message(
        order_id=order_id,
        name=request.name,
        address=request.address.value,
        phone=request.phone,
        items=items_for_telegram,
        subtotal=subtotal,
        delivery_charge=DELIVERY_CHARGE,
        total_price=total_price
    )
    
    return CreateOrderResponse(
        order_id=order_id,
        name=request.name,
        address=request.address,
        phone=request.phone,
        items=items_response,
        subtotal=subtotal,
        delivery_charge=DELIVERY_CHARGE,
        total_price=total_price,
        message=message
    )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Online Delivery System"}


@router.get("/items")
async def get_items():
    """Get all available items."""
    from backend.utils.items import get_items_catalog
    return get_items_catalog()