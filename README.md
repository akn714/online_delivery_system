# Online Delivery Registration System

A full-stack delivery order system with FastAPI backend, Supabase database, and Telegram bot integration.

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration (see Configuration section below)
uvicorn main:app --reload
```

### Database Setup
```bash
cd backend
python setup_database.py
```
Then copy the SQL output and run it in your Supabase SQL Editor.

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
│   ├── main.py              # FastAPI app entry point
│   ├── routes/
│   │   ├── auth.py          # Authentication endpoints
│   │   └── orders.py        # Order endpoints
│   ├── services/
│   │   └── telegram.py      # Telegram bot service
│   ├── models/
│   │   └── order.py         # Pydantic models
│   ├── database/
│   │   └── supabase_client.py # Supabase client
│   ├── setup_database.py    # Database setup script
│   ├── utils/
│   │   └── items.py         # Items catalog
│   └── requirements.txt
├── frontend/
│   └── index.html           # Order form UI
├── .env.example             # Environment template
└── README.md
```

## 🔧 Configuration

### Step 1: Get Supabase Credentials

1. Go to [supabase.com](https://supabase.com) and create a new project
2. After project creation, go to **Project Settings** → **API**
3. Copy the following values:
   - **Project URL** → Use as `SUPABASE_URL`
   - **anon public** (under "Project API keys") → Use as `SUPABASE_KEY`

### Step 2: Configure .env File

Copy `.env.example` to `.env` and fill in all values:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Delivery Configuration
DELIVERY_CHARGE=15

# Server Configuration
PORT=4000
```

### Step 3: Create Database Tables

Run the setup script and execute the SQL in Supabase:
```bash
cd backend
python setup_database.py
```

Then copy the SQL output and run it in your Supabase SQL Editor (found in the Supabase dashboard under "SQL Editor").

## 📦 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/login` | Login user |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/orders` | Create new order |
| GET | `/api/orders` | Get user's orders |
| GET | `/api/orders/{order_id}` | Get specific order |
| GET | `/api/health` | Health check |

## 🛠️ Tech Stack
- **Backend**: FastAPI, Pydantic, Supabase
- **Frontend**: HTML, CSS, Vanilla JS
- **Database**: Supabase (PostgreSQL)
- **Notifications**: Telegram Bot