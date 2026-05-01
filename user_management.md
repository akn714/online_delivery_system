Task: Implement user authentication and a "Your Orders" section for the platform, along with order tracking via OTP.

Overview:
Enhance the existing platform by adding user account management, order handling, and OTP-based order identification. Use Supabase as the primary database. You may modify both frontend and backend as needed.

---

USER AUTHENTICATION:
- Implement customer account handling.
- Store user details in Supabase.
- Refer to @file:user.md for the base schema.
- Extend the schema with additional fields if required (e.g., OTP, timestamps).
- Passwords must be securely encrypted.
- Ensure linkage between users and their orders.

---

OTP REQUIREMENT:
- Generate a unique 4-digit OTP when a user places an order.
- Display this OTP in the "Your Orders" section for the user.
- Send the OTP along with order details to a Telegram bot.

---

FRONTEND FLOW:
1. User enters personal details.
2. User selects items.
3. User clicks "Proceed to Payments".
4. Display QR code and input field.
5. User completes payment and enters transaction ID.
6. User clicks "Place Order".
7. User navigates to "Your Orders" to view their order and OTP.

---

BACKEND FLOW:
1. Receive order details from frontend.
2. Generate a unique 4-digit OTP.
3. Store order along with user ID and OTP.
4. Send order details + OTP to Telegram bot (chat ID).

---

DATABASE DESIGN:
This is given in @file:user.md file.


ADDITIONAL NOTES:
- You may create additional tables if needed.
- Store API keys and configs in Supabase .env variables.
- You may use Node.js for and frontend if required. (use only python for backend, don't change that)
- Ensure clean integration between authentication, order flow, and Telegram bot.
- Do not open the .env file, just add the required fields or variables in .env.example file, I'll copy from that file.

Objective:
A fully functional system where users can authenticate, place orders, and track them using a unique OTP.
