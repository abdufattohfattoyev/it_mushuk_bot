import sqlite3

DATABASE = "users.db"

def init_db():
    """Ma'lumotlar bazasi va jadvallarni yaratish."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Foydalanuvchilar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        username TEXT,
        full_name TEXT,
        is_active INTEGER DEFAULT 0
    )
    """)

    # Faol foydalanuvchilar loglari
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username, full_name):
    """Foydalanuvchini bazaga qo'shish."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (user_id, username, full_name) VALUES (?, ?, ?)",
                       (user_id, username, full_name))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def log_activity(user_id, action):
    """Foydalanuvchi faoliyatini loglash."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO activity_logs (user_id, action) VALUES (?, ?)
    """, (user_id, action))
    conn.commit()
    conn.close()

def get_active_users():
    """Faol foydalanuvchilarni olish."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT DISTINCT user_id FROM activity_logs
    """)
    active_users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return active_users



def get_all_users():
    """Barcha foydalanuvchilarni olish."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""SELECT user_id FROM users""")  # Foydalanuvchilarni olish
    users = cursor.fetchall()  # Foydalanuvchilar ro'yxatini olish
    conn.close()
    return [user[0] for user in users]