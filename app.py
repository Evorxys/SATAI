from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS teachers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Routes
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/admin/create', methods=['GET', 'POST'])
def admin_create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Admin account created successfully!')
            return redirect(url_for('admin_login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!')
        finally:
            conn.close()
    return render_template('admin_create.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM admins")
    admins_exist = cursor.fetchone()[0] > 0
    message = None
    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        password = request.form['password']
        if action == 'login':
            cursor.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
            admin = cursor.fetchone()
            conn.close()
            if admin:
                session['admin'] = username
                flash('Logged in successfully!')
                return redirect(url_for('admin_dashboard'))
            else:
                message = 'Invalid login credentials'
        elif action == 'register' and not admins_exist:
            try:
                cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                flash('Admin account created successfully!')
                return redirect(url_for('admin_login'))
            except sqlite3.IntegrityError:
                message = 'Username already exists!'
            finally:
                conn.close()
    return render_template('admin_login.html', admins_exist=admins_exist, message=message)


@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins")
    admins = cursor.fetchall()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', admins=admins, students=students, teachers=teachers)

@app.route('/student/signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO students (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            flash('Student registered successfully!')
        except sqlite3.IntegrityError:
            flash('Email already exists!')
        conn.close()
    return render_template('student_signup.html')

@app.route('/teacher/signup', methods=['GET', 'POST'])
def teacher_signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO teachers (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            flash('Teacher registered successfully!')
        except sqlite3.IntegrityError:
            flash('Email already exists!')
        conn.close()
    return render_template('teacher_signup.html')

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE email = ? AND password = ?", (email, password))
        student = cursor.fetchone()
        conn.close()
        if student:
            session['student'] = email
            flash('Logged in successfully!')
            return redirect(url_for('homepage'))
        else:
            flash('Invalid login credentials')
    return render_template('student_login.html')

@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers WHERE email = ? AND password = ?", (email, password))
        teacher = cursor.fetchone()
        conn.close()
        if teacher:
            session['teacher'] = email
            flash('Logged in successfully!')
            return redirect(url_for('homepage'))
        else:
            flash('Invalid login credentials')
    return render_template('teacher_login.html')

@app.route('/signup_them')
def signup_them():
    return render_template('signup_them.html')

@app.route('/login_them')
def login_them():
    return render_template('login_them.html')

@app.route('/admin/edit/<int:id>', methods=['POST'])
def edit_admin(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    username = request.form['username']
    password = request.form['password']
    cursor.execute("UPDATE admins SET username = ?, password = ? WHERE id = ?", (username, password, id))
    conn.commit()
    conn.close()
    flash('Admin updated successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_admin(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admins WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Admin deleted successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/student/edit/<int:id>', methods=['POST'])
def edit_student(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cursor.execute("UPDATE students SET name = ?, email = ?, password = ? WHERE id = ?", (name, email, password, id))
    conn.commit()
    conn.close()
    flash('Student updated successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/student/delete/<int:id>', methods=['POST'])
def delete_student(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Student deleted successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/teacher/edit/<int:id>', methods=['POST'])
def edit_teacher(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cursor.execute("UPDATE teachers SET name = ?, email = ?, password = ? WHERE id = ?", (name, email, password, id))
    conn.commit()
    conn.close()
    flash('Teacher updated successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/teacher/delete/<int:id>', methods=['POST'])
def delete_teacher(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teachers WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Teacher deleted successfully!')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
