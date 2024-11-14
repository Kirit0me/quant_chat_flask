from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from utils.db import get_db_connection
import datetime

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

@chat_bp.route('/send_message', methods=['POST'])
def send_message():
    sender = session.get('username')
    recipient = request.form.get('recipient')
    message = request.form.get('message')

    if not sender or not recipient or not message:
        return jsonify({'error': 'Invalid data'}), 400

    # Save message to database or temporary storage
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now()
    cursor.execute("INSERT INTO texts (sender, recipient, messages, timestamp) VALUES (%s, %s, %s, %s);",
                   (sender, recipient, message, timestamp))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'success': True})

@chat_bp.route('/fetch_messages')
def fetch_messages():
    sender = session.get('username')
    recipient = request.args.get('recipient')

    if not sender or not recipient:
        return jsonify([])

    # Fetch messages between the sender and recipient
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sender, messages, timestamp 
        FROM texts
        WHERE (sender = %s AND recipient = %s) 
           OR (sender = %s AND recipient = %s) 
        ORDER BY timestamp;
    """, (sender, recipient, recipient, sender))
    messages = cursor.fetchall()
    cursor.close()
    conn.close()

    # Format messages for JSON response
    message_list = [{'sender': row[0], 'message': row[1], 'timestamp': row[2].strftime("%Y-%m-%d %H:%M:%S")}
                    for row in messages]

    return jsonify(message_list)
