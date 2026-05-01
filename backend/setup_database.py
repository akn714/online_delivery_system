# """
# Database setup script for Supabase.
# Run this script to create the required tables in your Supabase project.

# Usage:
#     python setup_database.py
# """
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# SQL statements to create tables
CREATE_TABLES_SQL = """
-- Users table for customer authentication
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Orders table for storing order details
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    items JSONB NOT NULL,
    subtotal INTEGER NOT NULL,
    delivery_charge INTEGER NOT NULL,
    total_price INTEGER NOT NULL,
    transaction_id TEXT NOT NULL,
    otp TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (adjust as needed for production)
CREATE POLICY "Enable read access for all users" ON users FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON users FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable read access for all orders" ON orders FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all orders" ON orders FOR INSERT WITH CHECK (true);

-- Create index on user_id for faster order lookups
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at DESC);
"""


def setup_database():
    """Setup database tables using Supabase REST API."""
    import httpx
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        return False
    
    # Supabase uses POST to run RPC or direct SQL via REST API
    # We'll use the pg_catalog to execute SQL
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    # Note: Direct SQL execution requires pg_exec extension or using Supabase CLI
    # For production, it's recommended to run these SQL commands in Supabase SQL Editor
    
    print("=" * 60)
    print("SUPABASE DATABASE SETUP")
    print("=" * 60)
    print("\nTo create the required tables, run the following SQL")
    print("in your Supabase project's SQL Editor:\n")
    print("-" * 60)
    print(CREATE_TABLES_SQL)
    print("-" * 60)
    print("\nAlternatively, you can use Supabase CLI:")
    print("  supabase db push")
    print("\nOr connect to your database directly and run the SQL.")
    print("=" * 60)
    
    return True


def create_tables_via_api():
    """Create tables using Supabase Python client."""
    try:
        from supabase import create_client
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Check if users table exists
        try:
            supabase.table("users").select("id").limit(1).execute()
            print("✓ Users table already exists")
        except Exception:
            print("✗ Users table does not exist - please create it via SQL Editor")
        
        # Check if orders table exists
        try:
            supabase.table("orders").select("id").limit(1).execute()
            print("✓ Orders table already exists")
        except Exception:
            print("✗ Orders table does not exist - please create it via SQL Editor")
            
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ROCKET07 DELIVERY SYSTEM - DATABASE SETUP")
    print("=" * 60 + "\n")
    
    # Show the SQL that needs to be run
    setup_database()
    
    print("\n")