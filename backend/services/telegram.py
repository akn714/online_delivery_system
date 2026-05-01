import os
import httpx
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")
print(WEBHOOK_URL)


async def _telegram_api_call(method: str, payload: dict) -> dict:
    """Call Telegram Bot API and return parsed response."""
    if not BOT_TOKEN:
        return {"ok": False, "description": "Telegram bot token not configured"}

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            return response.json()
    except Exception as exc:
        return {"ok": False, "description": str(exc)}


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
    
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "Confirm Order",
                        "callback_data": f"confirm_order:{order_id}",
                    }
                ]
            ]
        },
    }
    result = await _telegram_api_call("sendMessage", payload)
    if result.get("ok"):
        return {"success": True, "message": "Order sent to Telegram"}
    return {"success": False, "error": result.get("description", "Unknown error")}


async def answer_callback_query(callback_query_id: str, text: str) -> None:
    """Send popup response for a Telegram callback query."""
    print('[+] answering callback query', text)
    await _telegram_api_call(
        "answerCallbackQuery",
        {"callback_query_id": callback_query_id, "text": text, "show_alert": False},
    )


async def get_webhook_info() -> dict:
    """Fetch Telegram webhook configuration/status."""
    print('[+] get webhook')
    return await _telegram_api_call("getWebhookInfo", {})


async def set_webhook(url: str) -> dict:
    """Set Telegram webhook to given HTTPS URL."""
    print('[+] webhook set')
    return await _telegram_api_call("setWebhook", {"url": url})


async def ensure_webhook_configured() -> dict:
    """
    Ensure webhook is configured when TELEGRAM_WEBHOOK_URL is provided.
    Returns API response dict for observability.
    """
    if not WEBHOOK_URL:
        return {"ok": False, "description": "TELEGRAM_WEBHOOK_URL not configured"}
    return await set_webhook(WEBHOOK_URL)


async def update_message_confirmation_status(chat_id: str, message_id: int, order_id: str) -> None:
    """Update Telegram message to show order confirmed and remove button."""
    await _telegram_api_call(
        "editMessageReplyMarkup",
        {"chat_id": chat_id, "message_id": message_id, "reply_markup": {"inline_keyboard": []}},
    )
    await _telegram_api_call(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": f"✅ Order `{order_id}` has been marked as *confirmed*.",
            "parse_mode": "Markdown",
        },
    )


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