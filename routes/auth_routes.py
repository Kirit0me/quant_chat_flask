from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import create_user, verify_user

# Define the blueprint and register routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if create_user(username, password):
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for('auth.login'))  # Update this if the login route is under `auth`
        else:
            flash("Signup failed. Please try again.", "error")
    
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if verify_user(username, password):
            session['username'] = username  # Store the username in session
            flash("Login successful!", "success")
            return redirect(url_for('home_page'))  # Redirect to home_page after login
        else:
            flash("Invalid username or password.", "error")
    
    return render_template('login.html')    

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    flash("You have been logged out.")
    return redirect(url_for('auth.login'))  # Redirect to the login page after logout

