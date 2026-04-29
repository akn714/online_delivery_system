import os
import httpx
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


async def send_order_to_telegram(order_id: str, name: str, address: str, phone: str, 
                                   items: list, subtotal: int, delivery_charge: int, 
                                   total_price: int) -> dict:
    """
    Send order notification to admin via Telegram.
    """
    if not BOT_TOKEN or not CHAT_ID:
        return {"success": False, "error": "Telegram credentials not configured"}
    
    # Format items list
    items_text = "\n  • ".join([f"{item['name']} × {item['quantity']}" for item in items])
    
    message = f"""Thank you for placing your order with us. We appreciate your trust and are processing your request.

Here are your order details:

- Order ID: {order_id}
- Delivery Charges: ₹{delivery_charge}
- Total Price: ₹{total_price}

- Items Ordered:
  • {items_text}

Your order will be delivered shortly. If you have any questions, feel free to contact us."""
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            result = response.json()
            
            if response.status_code == 200 and result.get("ok"):
                return {"success": True, "message": "Order sent to Telegram"}
            else:
                return {"success": False, "error": result.get("description", "Unknown error")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def format_telegram_message(order_id: str, name: str, address: str, phone: str,
                             items: list, subtotal: int, delivery_charge: int,
                             total_price: int) -> str:
    """Format the order message for Telegram (for preview)."""
    items_text = "\n  • ".join([f"{item['name']} × {item['quantity']}" for item in items])
    
    return f"""Thank you for placing your order with us. We appreciate your trust and are processing your request.

Here are your order details:

- Order ID: {order_id}
- Delivery Charges: ₹{delivery_charge}
- Total Price: ₹{total_price}

- Items Ordered:
  • {items_text}

Your order will be delivered shortly. If you have any questions, feel free to contact us."""