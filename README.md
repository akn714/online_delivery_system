# Online Delivery Registration System

A full-stack delivery order system with FastAPI backend and Telegram bot integration.

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Telegram Bot Token and Chat ID
uvicorn main:app --reload
```

### Frontend
Simply open `frontend/index.html` in a browser, or serve it:
```bash
cd frontend
python -m http.server 8000
```

## 📁 Project Structure
```
delivery_system/
├── backend/
│   ├── main.py          # FastAPI app entry point
│   ├── routes/
│   │   └── orders.py    # Order endpoints
│   ├── services/
│   │   └── telegram.py  # Telegram bot service
│   ├── models/
│   │   └── order.py     # Pydantic models
│   ├── utils/
│   │   └── items.py     # Items catalog
│   └── requirements.txt
├── frontend/
│   └── index.html       # Order form UI
├── .env.example         # Environment template
└── README.md
```

## 🔧 Configuration
Edit `backend/.env`:
- `TELEGRAM_BOT_TOKEN` - Your bot token from BotFather
- `TELEGRAM_CHAT_ID` - Your chat ID to receive orders
- `DELIVERY_CHARGE` - Default: 15

## 📦 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/create-order` | Create new order |
| GET | `/api/health` | Health check |

## 🛠️ Tech Stack
- **Backend**: FastAPI, Pydantic, python-telegram-bot
- **Frontend**: HTML, CSS, Vanilla JS