from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "virtue_secret_key"

# ---------------------------
# DATABASE SETUP
# ---------------------------

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            service TEXT NOT NULL,
            message TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------------------
# ROUTES
# ---------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/process')
def process():
    return render_template('process.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        service = request.form.get('service')
        message = request.form.get('message')
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO inquiries (name, phone, email, service, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, phone, email, service, message, created_at))
        conn.commit()
        conn.close()

        flash("Your consultation request has been submitted successfully.")
        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/legal')
def legal():
    return render_template('legal.html')


@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM inquiries ORDER BY created_at DESC")
    inquiries = c.fetchall()

    conn.close()

    return render_template('admin.html', inquiries=inquiries)

if __name__ == '__main__':
    app.run(debug=True)