import psycopg2
from app.config import Config

def create_wallet(user_id, wallet_address, network):
    conn = psycopg2.connect(Config.SYSTEM_DB_URI)
    cur = conn.cursor()
    cur.execute("INSERT INTO monitored_wallets (user_id, wallet_address, network) VALUES (%s, %s, %s)", (user_id, wallet_address, network))
    conn.commit()
    cur.close()
    conn.close()

def delete_wallet(wallet_id):
    conn = psycopg2.connect(Config.SYSTEM_DB_URI)
    cur = conn.cursor()
    cur.execute("DELETE FROM monitored_wallets WHERE id = %s", (wallet_id,))
    conn.commit()
    cur.close()
    conn.close()
