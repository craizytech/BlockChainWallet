import psycopg2
from app.config import Config

def create_user(email, password):
    conn = psycopg2.connect(Config.SYSTEM_DB_URI)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
    conn.commit()
    cur.close()
    conn.close()

def get_user_by_email(email):
    conn = psycopg2.connect(Config.SYSTEM_DB_URI)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user
