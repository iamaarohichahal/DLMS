from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import re

app = Flask(__name__)

app.secret_key = 'mysecretkey'

# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password,))
        user = cursor.fetchone()
        conn.close()
        if user:
            if user['username'] == 'admin':  # Assuming 'username' is used for role checking
                session['loggedin'] = True
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['email'] = user['email']
                message = 'Login successful!'
                return redirect(url_for('users'))
            else:
                message = 'This login is for admins only'
        else:
            message = 'Please enter the correct email / password!'
    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('email', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/users", methods=['GET'])
def users():
    if 'loggedin' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        conn.close()
        return render_template("users.html", users=users)
    return redirect(url_for('login'))

@app.route("/view", methods=['GET'])
def view():
    if 'loggedin' in session:
        view_user_id = request.args.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (view_user_id,))
        user = cursor.fetchone()
        conn.close()
        return render_template("view.html", user=user)
    return redirect(url_for('login'))

@app.route("/loan", methods=['GET'])
def loan():
    if 'loggedin' in session:
        loan_user_id = request.args.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM loans WHERE user_id = ?', (loan_user_id,))
        loans = cursor.fetchall()
        conn.close()
        return render_template("loans.html", loans=loans, user_id=loan_user_id)
    return redirect(url_for('login'))

@app.route("/edit", methods=['GET', 'POST'])
def edit():
    msg = ''
    if 'loggedin' in session:
        edit_user_id = request.args.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (edit_user_id,))
        edit_user = cursor.fetchone()

        if request.method == 'POST' and 'username' in request.form and 'user_id' in request.form and 'role' in request.form and 'country' in request.form:
            username = request.form['username']
            role = request.form['role']
            country = request.form['country']
            user_id = request.form['user_id']
            if not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            else:
                cursor.execute('UPDATE users SET username = ?, role = ?, country = ? WHERE id = ?', (username, role, country, user_id,))
                conn.commit()
                conn.close()
                msg = 'User updated!'
                return redirect(url_for('users'))
        elif request.method == 'POST':
            msg = 'Please fill out the form!'

        conn.close()
        return render_template("edit.html", msg=msg, edit_user=edit_user)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
