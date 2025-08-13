from db import get_connection
from mysql.connector import Error

try:
    conn = get_connection()
    if conn.is_connected():
        print("✅ Connected to Railway MySQL!")
        print(f"📍 Host: {conn.server_host}, DB: {conn.database}")
    else:
        print("❌ Not connected 😭")
except Error as e:
    print(f"❌ MySQL Error: {e}")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("🔌 Connection closed.")
