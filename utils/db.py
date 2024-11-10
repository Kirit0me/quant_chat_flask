import psycopg2
import os

# Use environment variables for sensitive data or hardcode your Supabase URL temporarily
DATABASE_URL = "postgresql://postgres.uczrcjrxhmiwpkpolywj:Supabase%40123@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

def get_db_connection():
    """Establishes and returns a connection to the Supabase PostgreSQL database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None
