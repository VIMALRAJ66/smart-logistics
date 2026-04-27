import os
import random
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

# 🔒 SECURITY: Required for sessions on Render
app.secret_key = os.environ.get('SECRET_KEY', 'smart_logistics_2026_key')

# ---------------- DATABASE CONNECTION (AIVEN CLOUD) ----------------
db_config = {
    'host': 'logistics-db-rajssv004-c5d2.i.aivencloud.com',
    'port': 19272,
    'user': 'avnadmin',
    'password': 'AVNS_P-1ic66btBVDKEUFdn7',
    'database': 'defaultdb',
    'ssl_ca': 'ca.pem',     # This must match the file name you upload
    'ssl_verify_cert': True
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Exception as e:
        print(f"❌ Database Connection Error: {e}")
        return None

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')

        conn = get_db_connection()
        if conn:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pwd))
            account = cur.fetchone()
            conn.close()

            if account:
                session['loggedin'] = True
                session['username'] = user
                return redirect(url_for('dashboard'))
        
        return render_template("login.html", error="❌ Invalid Credentials")
            
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    new_user = request.form.get('new_user')
    new_pass = request.form.get('new_pass')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_user, new_pass))
            conn.commit()
            msg = "✅ Account Created! Please Login."
        except Exception as e:
            msg = f"❌ Error: {e}"
        finally:
            conn.close()
        return render_template("login.html", error=msg)
    return "Database Error"

@app.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('login_page'))

    conn = get_db_connection()
    if not conn: 
        return "Database Connection Failed"
    
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM trucks")
    rows = cur.fetchall()
    conn.close()

    values = {
        "trucks": len(rows),
        "parcels": len(rows) * 120,
        "weight": len(rows) * 900,
        "alerts": random.randint(0, 2),
        "location": "Chennai Hub"
    }
    return render_template("dashboard.html", rows=rows, v=values)

@app.route('/add', methods=['POST'])
def add():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO trucks (truck_no, driver, type, status) VALUES (%s, %s, %s, %s)", 
                    (request.form['truck'], request.form['driver'], request.form['type'], request.form['status']))
        conn.commit()
        conn.close()
    return redirect(url_for('dashboard'))

@app.route('/map/<int:id>')
def map_view(id):
    conn = get_db_connection()
    if conn:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM trucks WHERE id=%s", (id,))
        truck = cur.fetchone()
        conn.close()
        if truck:
            stats = {
                "location": random.choice(["Chennai Highway", "Bangalore City", "Salem Junction"]),
                "weight": random.randint(500, 3000),
                "parcels": random.randint(50, 200),
                "alert": random.choice(["No Alerts", "Speeding", "Low Fuel"])
            }
            return render_template("map.html", truck=truck, s=stats)
    return "Truck Not Found", 404

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    # On local, it uses this. On Render, gunicorn takes over.
    app.run(host='0.0.0.0', port=5000)