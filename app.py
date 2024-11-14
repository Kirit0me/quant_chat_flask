from flask import Flask, flash, render_template, session, redirect, url_for
from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp 
from utils.db import get_db_connection  

app = Flask(__name__)
app.secret_key = "supersecretkey"  

# Routes
@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/login')
def login():    
    return render_template('login.html') 

@app.route('/signup')
def signup():
    return render_template('signup.html') 

@app.route('/home_page')
def home_page():
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))  # Redirect to login if not authenticated
    
    # Fetch other users from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM messages WHERE username != %s;", (username,))
    users = [user[0] for user in cursor.fetchall()]  # Extract usernames from tuples
    cursor.close()
    conn.close()

    return render_template('home_page.html', username=username, users=users)
    
# Register the auth and chat blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(chat_bp, url_prefix='/chat')


if __name__ == '__main__':
     app.run(debug=True)
