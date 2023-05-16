from flask import Flask, render_template, request, redirect, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'
@app.route("/")
def home():
    return "<h1>Welcome Page</h1>"

# Database setup
def create_users_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       username TEXT NOT NULL,
                       password TEXT NOT NULL)''')
    conn.commit()
    conn.close()
def create_donors_table():
    conn = sqlite3.connect('donors.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS donors
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       type TEXT, 
                       donorname TEXT NOT NULL, 
                       donorsex TEXT, 
                       qty TEXT NOT NULL, 
                       dweight TEXT NOT NULL, 
                       donoremail TEXT NOT NULL, 
                       phone TEXT NOT NULL)''')
    conn.commit()
    conn.close()
@app.route("/index")
def index():
    username = session.get('username') or ''
    return render_template('index.html', username=username)
# Sign up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)", (name, username, password))
        conn.commit()
        conn.close()
        
        return redirect('/login')
    
    return render_template('signup.html')

@app.route('/register', methods =['POST','GET'])
def register():
    if request.method == 'POST':
           if ((session.get('user_csrf') or 'notav') != request.form.get('csrfvalue', 'JJ')):
              pass #return render_template('register.html', csrfvalue=(session.get('user_csrf') or ''))
           type = request.form['blood_group']
           donorname = request.form['donorname']
           donorsex = request.form['gender']
           qty = request.form['qty']
           dweight = request.form['dweight']
           email = request.form['email']
           phone = request.form['phone']
        
           conn = sqlite3.connect('donors.db')
           cursor = conn.cursor()
           cursor.execute("INSERT INTO donors (type,donorname,donorsex,qty,dweight,donoremail,phone) VALUES (?,?,?,?,?,?,?)",(type,donorname,donorsex,qty,dweight,email,phone) )
           conn.commit()
           conn.close()
        
           return redirect('/register')
    
    return render_template('register.html', csrfvalue=(session.get('user_csrf') or ''))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            name = user[1]
            session['username'] = name
            session['user_csrf'] = random.choice(['0x11a', '0x2244b', '0x1acx'])
            #return f'Welcome, {name}!'
            return redirect('/index')
        else:
            return 'Invalid username or password'
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('donors.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM donors')
    donors = cur.fetchall()
    conn.close()
    return render_template('dashboard.html', donors=donors)

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        type = request.form['blood_group']
        
        conn = sqlite3.connect('donors.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT donorname FROM donors WHERE type=?", (type,))
        donors = cursor.fetchall()
        
        conn.close()
        
        return render_template('search.html', donors=donors)
    
    return render_template('search.html')

@app.route("/logout")
def logout():
    if ('username' in session):
        session.pop('username')
        session.pop('user_csrf')
    
    return redirect('/login')

@app.route("/delete", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        if ((session.get('user_csrf') or 'notav') != request.form.get('csrfvalue', 'JJ')):
              pass #return render_template('delete.html', csrfvalue=(session.get('user_csrf') or ''))
        id = request.form['id']

        conn = sqlite3.connect('donors.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM donors WHERE id=?", (id,))
        conn.commit()

        conn.close()

        return render_template('delete.html', csrfvalue=(session.get('user_csrf') or ''))

    return render_template('delete.html')
if __name__ == '__main__':
    create_users_table()
    create_donors_table()
    app.run(debug=True)
