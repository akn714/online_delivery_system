import os
import httpx
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


async def send_order_to_telegram(order_id: str, otp: str, name: str, address: str, phone: str, 
                                   items: list, subtotal: int, delivery_charge: int, 
                                   total_price: int, transaction_id: str) -> dict:
    """
    Send order notification to admin via Telegram.
    """
    if not BOT_TOKEN or not CHAT_ID:
        return {"success": False, "error": "Telegram credentials not configured"}
    
    # Format items list
    items_text = "\n  • ".join([f"{item['name']} × {item['quantity']}" for item in items])
    
    message = f"""🛒 *NEW ORDER RECEIVED*

*Order ID:* `{order_id}`
*OTP:* `{otp}`

*Customer Details:*
• Name: {name}
• Phone: {phone}
• Address: {address}

*Order Details:*
• Transaction ID: `{transaction_id}`
• Subtotal: ₹{subtotal}
• Delivery: ₹{delivery_charge}
• *Total: ₹{total_price}*

*Items:*
  • {items_text}

_Track order using OTP: {otp}_"""
    
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


def format_telegram_message(order_id: str, otp: str, name: str, address: str, phone: str,
                             items: list, subtotal: int, delivery_charge: int,
                             total_price: int, transaction_id: str) -> str:
    """Format the order message for Telegram (for preview)."""
    items_text = "\n  • ".join([f"{item['name']} × {item['quantity']}" for item in items])
    
    return f"""🛒 Order Confirmed!

*Order ID:* {order_id}
*OTP:* {otp}

*Items:*
  • {items_text}

*Total:* ₹{total_price}

Use OTP *{otp}* to track your order."""