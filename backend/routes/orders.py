from fastapi import APIRouter, HTTPException, Header
from datetime import datetime
import uuid
import os
import random
from dotenv import load_dotenv

from models.order import (
    CreateOrderRequest, 
    CreateOrderResponse,
    OrderItemResponse,
    OrderListResponse
)
from services.telegram import send_order_to_telegram, format_telegram_message
from database.supabase_client import get_supabase

load_dotenv()

router = APIRouter(prefix="/api", tags=["orders"])

DELIVERY_CHARGE = int(os.getenv("DELIVERY_CHARGE", "15"))


def generate_otp() -> str:
    """Generate a unique 4-digit OTP."""
    return f"{random.randint(1000, 9999)}"


def generate_order_id() -> str:
    """Generate a unique order ID."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"ORD#{timestamp}-{uuid.uuid4().hex[:4].upper()}"


@router.post("/orders", response_model=CreateOrderResponse)
async def create_order(request: CreateOrderRequest, authorization: str = Header(None)):
    """
    Create a new order and send notification to Telegram.
    """
    supabase = get_supabase()
    
    # Generate unique order ID and OTP
    order_id = generate_order_id()
    otp = generate_otp()
    
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
    
    # Format items for storage and Telegram
    items_for_storage = [
        {"name": item.name, "quantity": item.quantity, "price": item.price}
        for item in request.items
    ]
    
    items_for_telegram = [
        {"name": item.name, "quantity": item.quantity}
        for item in request.items
    ]
    
    # Create order record for Supabase
    order_record = {
        "id": order_id,
        "user_id": request.user_id,  # Can be None for guest users
        "name": request.name,
        "phone": request.phone,
        "address": request.address.value,
        "items": items_for_storage,
        "subtotal": subtotal,
        "delivery_charge": DELIVERY_CHARGE,
        "total_price": total_price,
        "transaction_id": request.transaction_id,
        "otp": otp,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    # Store order in Supabase
    result = supabase.table("orders").insert(order_record).execute()
    
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create order")
    
    # Send to Telegram (async, don't wait for success to return)
    await send_order_to_telegram(
        order_id=order_id,
        otp=otp,
        name=request.name,
        address=request.address.value,
        phone=request.phone,
        items=items_for_telegram,
        subtotal=subtotal,
        delivery_charge=DELIVERY_CHARGE,
        total_price=total_price,
        transaction_id=request.transaction_id
    )
    
    # Format message for response
    message = format_telegram_message(
        order_id=order_id,
        otp=otp,
        name=request.name,
        address=request.address.value,
        phone=request.phone,
        items=items_for_telegram,
        subtotal=subtotal,
        delivery_charge=DELIVERY_CHARGE,
        total_price=total_price,
        transaction_id=request.transaction_id
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
        otp=otp,
        message=message,
        status="pending",
        transaction_id=request.transaction_id
    )


@router.get("/orders", response_model=OrderListResponse)
async def get_orders(user_id: str = None, authorization: str = Header(None)):
    """
    Get orders for a specific user.
    """
    print(user_id)
    supabase = get_supabase()
    
    query = supabase.table("orders").select("*")
    
    if user_id:
        query = query.eq("user_id", user_id)
    
    # Order by created_at descending
    query = query.order("created_at", desc=True)
    
    result = query.execute()
    
    orders = []
    for order in result.data:
        items = [
            OrderItemResponse(
                name=item["name"],
                quantity=item["quantity"],
                price=item["price"]
            )
            for item in order.get("items", [])
        ]
        
        orders.append(CreateOrderResponse(
            order_id=order["id"],
            name=order["name"],
            address=DeliveryAddress(order["address"]),
            phone=order["phone"],
            items=items,
            subtotal=order["subtotal"],
            delivery_charge=order["delivery_charge"],
            total_price=order["total_price"],
            otp=order["otp"],
            message="",
            status=order.get("status", "pending"),
            transaction_id=order.get("transaction_id", "")
        ))
    
    return OrderListResponse(
        orders=orders,
        total=len(orders)
    )


@router.get("/orders/{order_id}", response_model=CreateOrderResponse)
async def get_order(order_id: str, authorization: str = Header(None)):
    """
    Get a specific order by ID.
    """
    supabase = get_supabase()
    
    result = supabase.table("orders").select("*").eq("id", order_id).execute()
    
    if not result.data or len(result.data) == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order = result.data[0]
    
    items = [
        OrderItemResponse(
            name=item["name"],
            quantity=item["quantity"],
            price=item["price"]
        )
        for item in order.get("items", [])
    ]
    
    return CreateOrderResponse(
        order_id=order["id"],
        name=order["name"],
        address=DeliveryAddress(order["address"]),
        phone=order["phone"],
        items=items,
        subtotal=order["subtotal"],
        delivery_charge=order["delivery_charge"],
        total_price=order["total_price"],
        otp=order["otp"],
        message="",
        status=order.get("status", "pending"),
        transaction_id=order.get("transaction_id", "")
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


# Import DeliveryAddress for type hints
from models.order import DeliveryAddress