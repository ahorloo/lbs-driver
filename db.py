import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

# 🔗 Connect to the Railway MySQL DB
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# 📦 Fetch all trips from the DB
def get_all_trips():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM trips"
        cursor.execute(query)
        trips = cursor.fetchall()
        return trips
    except Error as err:
        print("❌ Database Error:", err)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
