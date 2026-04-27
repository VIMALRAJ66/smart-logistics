import mysql.connector

# CONNECT TO YOUR AIVEN CLOUD DATABASE
config = {
    'host': 'logistics-db-rajssv004-c5d2.i.aivencloud.com', # .i. for India
    'port': 19272,
    'user': 'avnadmin',
    # FIXED: Changed 'l' (lion) to '1' (one)
    'password': 'AVNS_P-1ic66btBVDKEUFdn7', 
    'database': 'defaultdb',
    'ssl_disabled': False
}

try:
    print("Connecting to Aiven Cloud...")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # 1. CREATE USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        password VARCHAR(100)
    );""")

    # 2. CREATE TRUCKS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trucks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        truck_no VARCHAR(20),
        driver VARCHAR(50),
        type VARCHAR(20),
        status VARCHAR(20)
    );""")

    # 3. CREATE ADMIN ACCOUNT
    cursor.execute("INSERT IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")
    
    conn.commit()
    print("✅ SUCCESS! Tables created.")
    conn.close()

except Exception as e:
    print(f"❌ Error: {e}")