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

def send_eth(user_id, data):
    sender_wallet_id = data.get('sender_wallet_id')
    recipient_wallet_id = data.get('recipient_wallet_id')
    amount_sent = data.get('amount_sent')
    transaction_hash = data.get('transaction_hash')
    # Other transaction details
    
    try:
        conn = get_db_connection('eth_db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO eth_blockchain_transactions (transaction_hash, timestamp, block_number, transaction_index) VALUES (%s, now(), %s, %s) RETURNING id",
            (transaction_hash, data.get('block_number'), data.get('transaction_index'))
        )
        transaction_id = cur.fetchone()[0]
        
        cur.execute(
            "INSERT INTO eth_transaction_inputs (transaction_id, sender_wallet_id, amount_sent) VALUES (%s, %s, %s)",
            (transaction_id, sender_wallet_id, amount_sent)
        )
        
        cur.execute(
            "INSERT INTO eth_transaction_outputs (transaction_id, recipient_wallet_id, amount_received) VALUES (%s, %s, %s)",
            (transaction_id, recipient_wallet_id, amount_sent)  # assuming amount_sent equals amount_received for simplicity
        )
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "ETH transaction sent successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def receive_eth(user_id, data):
    # Implement receive ETH logic if different from send_eth
    pass

def send_solana(user_id, data):
    sender_wallet_id = data.get('sender_wallet_id')
    recipient_wallet_id = data.get('recipient_wallet_id')
    amount_sent = data.get('amount_sent')
    transaction_hash = data.get('transaction_hash')
    # Other transaction details
    
    try:
        conn = get_db_connection('solana_db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO solana_blockchain_transactions (transaction_hash, timestamp, block_number, transaction_index) VALUES (%s, now(), %s, %s) RETURNING id",
            (transaction_hash, data.get('block_number'), data.get('transaction_index'))
        )
        transaction_id = cur.fetchone()[0]
        
        cur.execute(
            "INSERT INTO solana_transaction_inputs (transaction_id, sender_wallet_id, amount_sent) VALUES (%s, %s, %s)",
            (transaction_id, sender_wallet_id, amount_sent)
        )
        
        cur.execute(
            "INSERT INTO solana_transaction_outputs (transaction_id, recipient_wallet_id, amount_received) VALUES (%s, %s, %s)",
            (transaction_id, recipient_wallet_id, amount_sent)  # assuming amount_sent equals amount_received for simplicity
        )
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Solana transaction sent successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def receive_solana(user_id, data):
    # Implement receive Solana logic if different from send_solana
    pass

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
