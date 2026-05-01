DATABASE DESIGN:

# User Schema (from @file:user.md)
- User ID (Primary Key)
- Name
- Phone No.
- Password (encrypted)
- Fields to link user with orders
- Add more fields if required

# Order Schema
- Order ID (Primary Key)
- User ID (Foreign Key)
- Items (JSON or structured format)
- Transaction ID
- OTP (4-digit)
- Timestamp
- Status (optional)
