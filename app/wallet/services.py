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

def add_wallet(user_id, data):
    wallet_address = data.get('wallet_address')
    network = data.get('network')

    if not wallet_address or not network:
        return jsonify({"error": "wallet_address and network are required"}), 400
    
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

def delete_wallet(user_id, data):
    wallet_id = data.get('wallet_id')
    
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM monitored_wallets WHERE id = %s AND user_id = %s",
            (wallet_id, user_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Wallet deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_wallets(user_id):
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM monitored_wallets WHERE user_id = %s", (user_id,))
        wallets = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"wallets": wallets}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
