from database.connection import get_connection
from utils.security import hash_password

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # TABELA USERS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # =========================
    # USUÁRIO ADMIN PADRÃO
    # =========================
    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    user = cursor.fetchone()

    if not user:
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (
            "admin",
            hash_password("123"),
            "admin"
        ))

        print("✅ Usuário admin criado (admin / 123)")

    conn.commit()
    conn.close()