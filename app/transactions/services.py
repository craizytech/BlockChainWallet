import psycopg2
from flask import jsonify
from app.config import Config
from datetime import datetime
from flask_jwt_extended import create_access_token

def get_db_connection(db_name):
    conn = psycopg2.connect(
        dbname=db_name,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )
    return conn

def send_eth(user_id, data):
    try:
        transaction_hash = data.get('transaction_hash')
        wallet_assets = data.get('wallet_assets')
        token_names = data.get('token_names')
        value = data.get('value')
        status = data.get('status')
        block_number = data.get('block_number')
        fee = data.get('fee')
        transaction_index = data.get('transaction_index')
        input_data = data.get('input_data')
        signatures = data.get('signatures')
        timestamp = datetime.now()  # Current timestamp

        if not transaction_hash or not wallet_assets or not value or not timestamp:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection(Config.ETH_DB_NAME)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO eth_blockchain_transactions (transaction_hash, wallet_assets, token_names, value, timestamp, status, block_number, fee, transaction_index, input_data, signatures) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (transaction_hash, wallet_assets, token_names, value, timestamp, status, block_number, fee, transaction_index, input_data, signatures)
        )
        transaction_id = cur.fetchone()[0]

        sender_wallet_id = data.get('sender_wallet_id')
        recipient_wallet_id = data.get('recipient_wallet_id')
        amount_sent = data.get('amount_sent')
        amount_received = data.get('amount_received')

        if sender_wallet_id and amount_sent:
            cur.execute(
                "INSERT INTO eth_transaction_inputs (transaction_id, sender_wallet_id, amount_sent) VALUES (%s, %s, %s)",
                (transaction_id, sender_wallet_id, amount_sent)
            )

        if recipient_wallet_id and amount_received:
            cur.execute(
                "INSERT INTO eth_transaction_outputs (transaction_id, recipient_wallet_id, amount_received) VALUES (%s, %s, %s)",
                (transaction_id, recipient_wallet_id, amount_received)
            )

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Transaction sent successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def send_solana(user_id, data):
    try:
        transaction_hash = data.get('transaction_hash')
        wallet_assets = data.get('wallet_assets')
        token_names = data.get('token_names')
        timestamp = datetime.now()  # Current timestamp
        block_number = data.get('block_number')
        fee = data.get('fee')
        transaction_index = data.get('transaction_index')
        program_data = data.get('program_data')
        signatures = data.get('signatures')

        if not transaction_hash or not wallet_assets or not timestamp:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection(Config.SOLANA_DB_NAME)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO solana_blockchain_transactions (transaction_hash, wallet_assets, token_names, timestamp, block_number, fee, transaction_index, program_data, signatures) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (transaction_hash, wallet_assets, token_names, timestamp, block_number, fee, transaction_index, program_data, signatures)
        )
        transaction_id = cur.fetchone()[0]

        sender_wallet_id = data.get('sender_wallet_id')
        recipient_wallet_id = data.get('recipient_wallet_id')
        amount_sent = data.get('amount_sent')
        amount_received = data.get('amount_received')

        if sender_wallet_id and amount_sent:
            cur.execute(
                "INSERT INTO solana_transaction_inputs (transaction_id, sender_wallet_id, amount_sent) VALUES (%s, %s, %s)",
                (transaction_id, sender_wallet_id, amount_sent)
            )

        if recipient_wallet_id and amount_received:
            cur.execute(
                "INSERT INTO solana_transaction_outputs (transaction_id, recipient_wallet_id, amount_received) VALUES (%s, %s, %s)",
                (transaction_id, recipient_wallet_id, amount_received)
            )

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Transaction sent successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def get_transactions(user_id, wallet_address):
    try:
        conn_eth = get_db_connection('eth_db')
        cur_eth = conn_eth.cursor()
        cur_eth.execute(
            """
            SELECT
                t.transaction_hash,
                t.timestamp,
                sw.wallet_address AS sender_address,
                ti.amount_sent,
                rw.wallet_address AS recipient_address,
                to.amount_received
            FROM
                eth_blockchain_transactions t
            JOIN
                eth_transaction_inputs ti ON t.id = ti.transaction_id
            JOIN
                eth_wallets sw ON ti.sender_wallet_id = sw.id
            JOIN
                eth_transaction_outputs to ON t.id = to.transaction_id
            JOIN
                eth_wallets rw ON to.recipient_wallet_id = rw.id
            WHERE
                sw.wallet_address = %s OR rw.wallet_address = %s;
            """, (wallet_address, wallet_address)
        )
        eth_transactions = cur_eth.fetchall()
        cur_eth.close()
        conn_eth.close()

        conn_solana = get_db_connection('solana_db')
        cur_solana = conn_solana.cursor()
        cur_solana.execute(
            """
            SELECT
                t.transaction_hash,
                t.timestamp,
                sw.wallet_address AS sender_address,
                ti.amount_sent,
                rw.wallet_address AS recipient_address,
                to.amount_received
            FROM
                solana_blockchain_transactions t
            JOIN
                solana_transaction_inputs ti ON t.id = ti.transaction_id
            JOIN
                solana_wallets sw ON ti.sender_wallet_id = sw.id
            JOIN
                solana_transaction_outputs to ON t.id = to.transaction_id
            JOIN
                solana_wallets rw ON to.recipient_wallet_id = rw.id
            WHERE
                sw.wallet_address = %s OR rw.wallet_address = %s;
            """, (wallet_address, wallet_address)
        )
        solana_transactions = cur_solana.fetchall()
        cur_solana.close()
        conn_solana.close()

        return jsonify({"eth_transactions": eth_transactions, "solana_transactions": solana_transactions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
