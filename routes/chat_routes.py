from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.user_model import get_all_users

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
def chat_home():
    if 'username' not in session:
        flash("Please log in to access the chat.")
        return redirect(url_for('auth.login'))

    username = session['username']
    users = get_all_users(exclude=username)  # Fetch all users except the current user
    return render_template('chat.html', username=username, users=users)

@chat_bp.route('/chat/<recipient>')
def chat_with_user(recipient):
    if 'username' not in session:
        flash("Please log in to access the chat.")
        return redirect(url_for('auth.login'))
    
    username = session['username']
    return render_template('chat.html', username=username, recipient=recipient)
