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

def monitor_eth(user_id, data):
    wallet_address = data.get('wallet_address')
    transaction_hash = data.get('transaction_hash')
    # Additional data processing and monitoring logic here
    
    try:
        conn = get_db_connection('eth_db')
        cur = conn.cursor()
        # Insert or update logic for eth_db
        cur.execute(
            "INSERT INTO eth_blockchain_transactions (transaction_hash, wallet_assets, token_names, value, timestamp, status, block_number, fee, transaction_index, input_data, signatures) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (transaction_hash, "assets", "tokens", 0.0, 'now()', "status", 0, 0.0, 0, "input_data", "{}")
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "ETH transaction monitored successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def monitor_solana(user_id, data):
    wallet_address = data.get('wallet_address')
    transaction_hash = data.get('transaction_hash')
    # Additional data processing and monitoring logic here
    
    try:
        conn = get_db_connection('solana_db')
        cur = conn.cursor()
        # Insert or update logic for solana_db
        cur.execute(
            "INSERT INTO solana_blockchain_transactions (transaction_hash, wallet_assets, token_names, timestamp, block_number, fee, transaction_index, program_data, signatures) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (transaction_hash, "assets", "tokens", 'now()', 0, 0.0, 0, "program_data", "{}")
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Solana transaction monitored successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
