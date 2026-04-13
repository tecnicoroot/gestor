from database.connection import get_connection

class UserRepository:

    def create(self, username, password, role="user"):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (username, password, role))

        conn.commit()
        conn.close()

    def find_by_username(self, username):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, password, role
            FROM users WHERE username = ?
        """, (username,))

        user = cursor.fetchone()
        conn.close()

        return user
    
    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, role
            FROM users 
        """)

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "id": row[0],
                "username": row[1],
                "role": row[2]
            }
            for row in rows
        ]