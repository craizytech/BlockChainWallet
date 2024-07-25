import psycopg2
from flask import jsonify
from app.config import Config

def get_db_connection(db_name):
    conn = psycopg2.connect(
        dbname=db_name,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )
    return conn

def add_wallet(data):
    user_id = data.get('user_id')
    wallet_address = data.get('wallet_address')
    network = data.get('network')
    
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO monitored_wallets (user_id, wallet_address, network) VALUES (%s, %s, %s)",
            (user_id, wallet_address, network)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Wallet added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def remove_wallet(data):
    wallet_id = data.get('wallet_id')
    
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM monitored_wallets WHERE id = %s",
            (wallet_id,)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Wallet removed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
