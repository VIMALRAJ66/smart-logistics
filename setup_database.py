import mysql.connector
from werkzeug.security import generate_password_hash

# CONNECT TO YOUR AIVEN CLOUD DATABASE
config = {
    'host': 'logistics-db-rajssv004-c5d2.i.aivencloud.com',
    'port': 19272,
    'user': 'avnadmin',
    'password': 'AVNS_P-1ic66btBVDKEUFdn7', 
    'database': 'defaultdb',
    'ssl_ca': 'ca.pem',
    'ssl_verify_cert': True
}

try:
    print("🔄 Connecting to Aiven Cloud...")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # DELETE OLD TABLES (fresh start)
    print("🗑️  Dropping old tables...")
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS trucks")
    
    # 1. CREATE USERS TABLE (with correct password size)
    print("📝 Creating users table...")
    cursor.execute("""
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        password VARCHAR(255)
    );""")

    # 2. CREATE TRUCKS TABLE
    print("📝 Creating trucks table...")
    cursor.execute("""
    CREATE TABLE trucks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        truck_no VARCHAR(20),
        driver VARCHAR(50),
        type VARCHAR(20),
        status VARCHAR(20)
    );""")

    # 3. CREATE ADMIN ACCOUNT WITH HASHED PASSWORD
    print("👤 Creating admin user...")
    hashed_pwd = generate_password_hash('admin123')
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ('admin', hashed_pwd))
    
    # 4. ADD SAMPLE TRUCKS (for testing)
    print("🚛 Adding sample trucks...")
    sample_trucks = [
        ('TN-01-AB-1234', 'Rajesh Kumar', 'Container', 'In Transit'),
        ('TN-09-CD-5678', 'Suresh M', 'Tanker', 'Loading'),
        ('KA-05-EF-9012', 'Vijay S', 'Lorry', 'In Transit')
    ]
    cursor.executemany("INSERT INTO trucks (truck_no, driver, type, status) VALUES (%s, %s, %s, %s)", sample_trucks)
    
    conn.commit()
    print("\n✅ SUCCESS! Database setup complete.")
    print(f"✅ Admin account created (password length: {len(hashed_pwd)} chars)")
    print(f"✅ {len(sample_trucks)} sample trucks added")
    conn.close()

except Exception as e:
    print(f"\n❌ Error: {e}")