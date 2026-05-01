from fastapi import APIRouter, HTTPException, Header, Request
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
from services.telegram import (
    send_order_to_telegram,
    format_telegram_message,
    answer_callback_query,
    get_webhook_info,
    ensure_webhook_configured,
    update_message_confirmation_status,
)
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
    return f"ORD{timestamp}-{uuid.uuid4().hex[:4].upper()}"


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


@router.post("/telegram/callback")
async def handle_telegram_callback(request: Request):
    """
    Handle Telegram callback queries for order actions.

    Expected callback_data format: confirm_order:<order_id>
    """
    print('[+] telegram callback')
    try:
        payload = await request.json()
        callback_query = payload.get("callback_query")
        print(callback_query)


        if not callback_query:
            return {"ok": True, "message": "No callback_query in payload"}

        callback_data = callback_query.get("data", "")
        callback_query_id = callback_query.get("id")
        message = callback_query.get("message", {})
        chat_id = str(message.get("chat", {}).get("id", ""))
        message_id = message.get("message_id")

        if not callback_data.startswith("confirm_order:"):
            if callback_query_id:
                await answer_callback_query(callback_query_id, "Unsupported action.")
            return {"ok": True, "message": "Unsupported callback action"}

        order_id = callback_data.split(":", 1)[1]
        if not order_id:
            if callback_query_id:
                await answer_callback_query(callback_query_id, "Invalid order ID.")
            return {"ok": True, "message": "Invalid order ID"}

        supabase = get_supabase()
        lookup = supabase.table("orders").select("id,status").eq("id", order_id).execute()

        if not lookup.data:
            if callback_query_id:
                await answer_callback_query(callback_query_id, "Order not found.")
            return {"ok": True, "message": "Order not found"}

        current_status = lookup.data[0].get("status", "pending")
        if current_status == "confirmed":
            if callback_query_id:
                await answer_callback_query(callback_query_id, "Order already confirmed.")
            return {"ok": True, "message": "Order already confirmed"}

        update_result = (
            supabase.table("orders")
            .update({"status": "confirmed"})
            .eq("id", order_id)
            .execute()
        )

        # Some Supabase Python client versions don't return updated rows unless
        # specifically configured, so verify with a follow-up select.
        verify_after = supabase.table("orders").select("id,status").eq("id", order_id).execute()
        updated_rows = verify_after.data or []
        if not updated_rows or updated_rows[0].get("status") != "confirmed":
            # Verify current status to detect RLS/policy blocks clearly.
            current_after = verify_after.data[0].get("status") if verify_after.data else None
            error_hint = (
                "Update blocked (likely Supabase RLS policy). "
                "Allow UPDATE on orders or use SUPABASE_SERVICE_ROLE_KEY."
                if current_after != "confirmed"
                else "Order update did not return rows."
            )
            if callback_query_id:
                await answer_callback_query(callback_query_id, f"Failed to confirm: {error_hint}")
            return {"ok": False, "message": error_hint, "order_id": order_id}

        if callback_query_id:
            await answer_callback_query(callback_query_id, f"Order {order_id} confirmed.")
        if chat_id and message_id:
            await update_message_confirmation_status(chat_id, message_id, order_id)

        return {"ok": True, "message": f"Order {order_id} confirmed"}
    except Exception as exc:
        print(exc)
        return {"ok": False, "error": str(exc)}


@router.get("/telegram/debug-update")
async def telegram_debug_update(order_id: str):
    """
    Debug endpoint to validate whether backend can update order status.
    Does a no-op style write by setting status to its current value.
    """
    try:
        supabase = get_supabase()
        using_service_role_key = bool(os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

        print(order_id)
        current = supabase.table("orders").select("id,status").eq("id", order_id).execute()
        if not current.data:
            return {
                "ok": False,
                "message": "Order not found",
                "order_id": order_id,
                "using_service_role_key": using_service_role_key,
            }

        current_status = current.data[0].get("status", "pending")
        write_result = (
            supabase.table("orders")
            .update({"status": 'confirmed'})
            .eq("id", order_id)
            .execute()
        )

        post_check = supabase.table("orders").select("id,status").eq("id", order_id).execute()
        return {
            "ok": True,
            "order_id": order_id,
            "current_status_before": current_status,
            "current_status_after": (post_check.data[0].get("status") if post_check.data else None),
            "using_service_role_key": using_service_role_key,
            "update_response_data_length": len(write_result.data or []),
        }
    except Exception as exc:
        return {"ok": False, "order_id": order_id, "error": str(exc)}


@router.get("/telegram/webhook-info")
async def telegram_webhook_info():
    """Inspect Telegram webhook status for debugging callback issues."""
    result = await get_webhook_info()
    return result


@router.post("/telegram/configure-webhook")
async def telegram_configure_webhook():
    """Configure webhook from TELEGRAM_WEBHOOK_URL env variable."""
    result = await ensure_webhook_configured()
    return result


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