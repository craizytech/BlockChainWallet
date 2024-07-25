import psycopg2
from app.config import Config

def create_dashboard(user_id, name, type):
    conn = psycopg2.connect(Config.SYSTEM_DB_URI)
    cur = conn.cursor()
    cur.execute("INSERT INTO dashboards (user_id, name, type) VALUES (%s, %s, %s)", (user_id, name, type))
    conn.commit()
    cur.close()
    conn.close()

def delete_dashboard(dashboard_id):
    conn = psycopg2.connect(Config.SYSTEM_DB_URI)
    cur = conn.cursor()
    cur.execute("DELETE FROM dashboards WHERE id = %s", (dashboard_id,))
    conn.commit()
    cur.close()
    conn.close()

def get_transactions(wallet_id, network):
    if network == 'Ethereum':
        conn = psycopg2.connect(Config.ETH_DB_URI)
    elif network == 'Solana':
        conn = psycopg2.connect(Config.SOLANA_DB_URI)
    cur = conn.cursor()
    cur.execute("SELECT * FROM transaction_data WHERE wallet_id = %s", (wallet_id,))
    transactions = cur.fetchall()
    cur.close()
    conn.close()
    return transactions
