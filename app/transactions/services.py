import psycopg2
from flask import jsonify
from app.config import Config

def get_db_connection():
    conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )
    return conn

def get_transactions(wallet_address, network):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if network.lower() == 'ethereum':
            cur.execute(
                "SELECT block_hash, block_number, transaction_hash, from_address, to_address, value, gas, gas_price, timestamp FROM eth_transactions WHERE wallet_id IN (SELECT id FROM wallets WHERE wallet_address = %s)",
                (wallet_address,)
            )
        elif network.lower() == 'solana':
            cur.execute(
                "SELECT block_hash, block_number, transaction_hash, from_address, to_address, value, gas, gas_price, timestamp FROM solana_transactions WHERE wallet_id IN (SELECT id FROM wallets WHERE wallet_address = %s)",
                (wallet_address,)
            )
        else:
            return jsonify({"error": "Invalid network type"}), 400

        transactions = cur.fetchall()
        cur.close()
        conn.close()

        transactions_list = [
            {
                "block_hash": tx[0],
                "block_number": tx[1],
                "transaction_hash": tx[2],
                "from_address": tx[3],
                "to_address": tx[4],
                "value": tx[5],
                "gas": tx[6],
                "gas_price": tx[7],
                "timestamp": tx[8]
            } for tx in transactions
        ]
        return jsonify(transactions_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
