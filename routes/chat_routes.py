# routes/chat_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from utils.db import get_db_connection  

# Create a Blueprint for chat
chat_bp = Blueprint('chat', __name__, template_folder='templates')

@chat_bp.route('/chat_home')
def chat_home():
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))  # Redirect to login if not authenticated

    # Fetch the list of users from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM messages WHERE username != %s;", (username,))
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('chat.html', users=users)


@chat_bp.route('/chat_with_user/<recipient>', methods=['GET', 'POST'])
def chat_with_user(recipient):
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))  # Redirect to login if not authenticated

    # Handle sending messages
    if request.method == 'POST':
        message = request.form['message']
        # Save the message to the database (You'll need a function for this)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (sender, recipient, message) VALUES (%s, %s, %s);", 
                       (username, recipient, message))
        conn.commit()
        cursor.close()
        conn.close()

    # Fetch messages between the user and recipient
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sender, message, timestamp FROM messages WHERE (sender = %s AND recipient = %s) OR (sender = %s AND recipient = %s) ORDER BY timestamp;", 
                   (username, recipient, recipient, username))
    messages = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('chat.html', recipient=recipient, messages=messages)
