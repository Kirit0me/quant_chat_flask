from flask import Blueprint, render_template, session, redirect, url_for, request
from utils.db import get_db_connection

chat_bp = Blueprint('chat', __name__, template_folder='templates')

@chat_bp.route('/chat_home')
def chat_home():
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))

    # Fetch the list of other users from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT username FROM messages WHERE username != %s;", (username,))
    users = [user[0] for user in cursor.fetchall()]  # List of usernames
    cursor.close()
    conn.close()

    return render_template('chat.html', users=users, username=username)

# Route for initiating chat with a specific recipient
@chat_bp.route('/chat_with_user/<recipient>')
def chat_with_user(recipient):
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))

    return render_template('chat.html', recipient=recipient, username=username)
