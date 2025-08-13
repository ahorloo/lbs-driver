from db import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # get nice dict rows

    cursor.execute("SELECT * FROM trips LIMIT 10")
    rows = cursor.fetchall()

    if rows:
        print("✅ Found trips data:")
        for row in rows:
            print(row)
    else:
        print("⚠️ No data found in trips table.")

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
