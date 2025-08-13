import os

class Config:
    # 📁 Folder where uploaded CSVs will go
    UPLOAD_FOLDER = 'uploads'

    # 🛢️ MySQL DB connection settings
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'driver_logbook_db')
    DB_PORT = int(os.getenv('DB_PORT', 3306))  # default MySQL port

    # 🔒 Flask secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'p9v$X1!aZrT7qLmCw@3nB^Fs8dh')

    # 🧱 Route access password
    ACCESS_PASSWORD = os.getenv('ACCESS_PASSWORD', 'letmein123')
