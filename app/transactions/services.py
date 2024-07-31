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

def get_transactions(user_id, wallet_address, network):
    if not wallet_address or not network:
        return jsonify({"error": "wallet_address and network are required"}), 400

    try:
        if network == 'ethereum':
            conn = get_db_connection('eth_db')
            cur = conn.cursor()
            cur.execute(
                """
                SELECT
                    t.transaction_hash,
                    t.timestamp,
                    sw.wallet_address AS sender_address,
                    ti.amount_sent,
                    rw.wallet_address AS recipient_address,
                    "to".amount_received
                FROM
                    eth_blockchain_transactions t
                JOIN
                    eth_transaction_inputs ti ON t.id = ti.transaction_id
                JOIN
                    eth_wallets sw ON ti.sender_wallet_id = sw.id
                JOIN
                    eth_transaction_outputs "to" ON t.id = "to".transaction_id
                JOIN
                    eth_wallets rw ON "to".recipient_wallet_id = rw.id
                WHERE
                    sw.wallet_address = %s OR rw.wallet_address = %s;
                """, (wallet_address, wallet_address)
            )
            transactions = cur.fetchall()
            cur.close()
            conn.close()

        elif network == 'solana':
            conn = get_db_connection('solana_db')
            cur = conn.cursor()
            cur.execute(
                """
                SELECT
                    t.transaction_hash,
                    t.timestamp,
                    sw.wallet_address AS sender_address,
                    ti.amount_sent,
                    rw.wallet_address AS recipient_address,
                    "to".amount_received
                FROM
                    solana_blockchain_transactions t
                JOIN
                    solana_transaction_inputs ti ON t.id = ti.transaction_id
                JOIN
                    solana_wallets sw ON ti.sender_wallet_id = sw.id
                JOIN
                    solana_transaction_outputs "to" ON t.id = "to".transaction_id
                JOIN
                    solana_wallets rw ON "to".recipient_wallet_id = rw.id
                WHERE
                    sw.wallet_address = %s OR rw.wallet_address = %s;
                """, (wallet_address, wallet_address)
            )
            transactions = cur.fetchall()
            cur.close()
            conn.close()
        
        else:
            return jsonify({"error": "Invalid network specified"}), 400

        return jsonify({"transactions": transactions, "network": network}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
