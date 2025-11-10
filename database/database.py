import sqlite3
import os

# ----------------------------
# Get Database Connection
# ----------------------------
def get_db_connection():
    # This ensures the DB file is always inside the database folder
    db = sqlite3.connect("EMS.db")
    return db


# ----------------------------
# Create Tables (Run Once)
# ----------------------------
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('user', 'admin')) NOT NULL
        )
    """)

    # Events Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT,
            time TEXT,
            price INTEGER,
            total_tickets INTEGER,
            tickets_available INTEGER,
            venue TEXT,
            capacity INTEGER
        )
    """)

    # Bookings Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            event_id INTEGER,
            num_tickets INTEGER,
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL DEFAULT 'confirmed',
            total_price REAL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


# ----------------------------
# Run initialization if executed directly
# ----------------------------
if __name__ == "__main__":
    initialize_database()
