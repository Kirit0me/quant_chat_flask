from utils.db import get_db_connection

def create_user(username, password):
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

def get_all_users(exclude_username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM messages WHERE username != %s;", (exclude_username,))
    users = [user[0] for user in cursor.fetchall()]
    cursor.close()
    conn.close()
    return users
