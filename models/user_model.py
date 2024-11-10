from utils.db import get_db_connection

def create_user(username, password):
    """Inserts a new user into the database."""
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (username, password) VALUES (%s, %s);
        ''', (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error creating user:", e)
        return False

def verify_user(username, password):
    """Verifies if the user exists in the database with the correct password."""
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM messages WHERE username = %s AND password = %s;
        ''', (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user is not None
    except Exception as e:
        print("Error verifying user:", e)
        return False
