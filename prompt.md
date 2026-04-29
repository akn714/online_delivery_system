# Online Delivery Registration System (Full-Stack + Telegram Integration)

Build a clean, minimal, and production-ready **Online Delivery Registration System** consisting of:
- Frontend (form-based UI)
- Backend (FastAPI)
- Telegram Bot integration
- (Optional Phase 2: Supabase database)

---

## 🎯 Objective
Users submit an order through a web form.  
The backend processes the data, calculates pricing, formats a structured message, and sends it to an admin via a Telegram bot.

---

## 🧩 System Architecture
Frontend → FastAPI Backend → Telegram Bot → Admin

---

## ⚙️ Requirements

## 1. Frontend
Create a simple responsive UI (HTML/CSS/JS):

### Form Fields:
- Name (text)
- Delivery Address (dropdown):
  - BH1, BH2, BH3 (Boys Hostel)
  - GH1 (Girls Hostel)
- Phone Number (number/string)

### Items Section:
- Display items categorized:
  - Stationary
  - Grocery
  - etc.
- Each category should contain their items listed in the items.md file

Each item should include:
- Item name
- Quantity input
- Price display
- Checkbox

### Behavior:
- User selects items via checkbox
- Enters quantity for each selected item
- On submit → send POST request to backend

---

## 2. Backend (FastAPI)

### Endpoint:
POST /create-order

### Responsibilities:
- Accept JSON payload from frontend
- Validate required fields
- Process selected items
- Calculate:
  - Subtotal
  - Delivery Charges = ₹15 (fixed)
  - Total Price = subtotal + delivery

### Generate Order ID:
- Unique ID (UUID or timestamp-based): eg. "Order#(unique id)"

---

## 🧾 Message Formatting (STRICT FORMAT)

Format the message EXACTLY like this:
"
Thank you for placing your order with us. We appreciate your trust and are processing your request.

Here are your order details:

- Order ID: {{order_id}}
- Delivery Charges: ₹15
- Total Price: ₹{{total_price}}

- Items Ordered:
  • {{item_1}} × {{qty}}
  • {{item_2}} × {{qty}}

Your order will be delivered shortly. If you have any questions, feel free to contact us.
"

---

## 3. Telegram Bot Integration

### Requirements:
- Use Telegram Bot API
- Send formatted message to admin chat

### Steps: (Skip this, this will be done by me)
1. Create bot using BotFather
2. Store BOT_TOKEN and CHAT_ID in environment variables
3. Backend sends POST request to:
   https://api.telegram.org/bot<TOKEN>/sendMessage

---

## 4. Environment Variables (.env)

Create a `.env` file with:

- TELEGRAM_BOT_TOKEN=
- TELEGRAM_CHAT_ID=
- DELIVERY_CHARGE=15
- and other variables you need to setup this project

---

## 🚀 Phase 2 (Optional: Database - Supabase)

Store each order with:
- Order ID (primary key)
- Name
- Phone Number
- Address
- Items (string format):
  Example:
  "Apple (1kg), Banana (2kg), Hair Oil (1 bottle)"
- Total Price

---

## 🧠 Implementation Notes

- Use Pydantic models in FastAPI
- Ensure clean separation of concerns:
  - routes/
  - services/
  - utils/
- Handle empty item selections
- Validate quantity > 0
- Keep code modular and readable

---

## 📦 Expected Output

- Fully working frontend form
- FastAPI backend with one main route
- Telegram bot integration sending real-time order messages
- Clean and maintainable code structure

---

## 🔥 Bonus (IMP)

- Add loading state on submit
- Add success/failure toast messages
- Input validation on frontend
- Prevent duplicate submissions
- Deploy backend (Render / Railway) (Leave this, I'll do it)
