from flask import Flask, flash, render_template, session, redirect, url_for
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session and flash messages

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
        return redirect(url_for('auth.login'))
    
    # Fetch other users from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username != %s;", (username,))
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('home_page.html', username=username, users=[user[0] for user in users])

    
# Register the auth blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
