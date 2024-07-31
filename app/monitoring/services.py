import asyncio
import aiohttp
import threading
import psycopg2
from flask import jsonify, current_app
from app.config import Config
import datetime

def get_db_connection(db_name):
    conn = psycopg2.connect(
        dbname=db_name,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )
    return conn

def is_wallet_monitored(wallet_address, network):
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM monitored_wallets WHERE wallet_address = %s AND network = %s", (wallet_address, network))
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count > 0
    except Exception as e:
        current_app.logger.error(f"Error checking if wallet is monitored: {e}")
        return False

async def fetch_eth_transaction_data(session, wallet_address):
    try:
        async with session.post(Config.ETH_API_URL, json={
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": ["latest", True],
            "id": 1
        }) as response:
            if response.status != 200:
                current_app.logger.error(f"Error: Received status code {response.status}")
                return []
            data = await response.json()
            
            # The JSON response from the API
            block = data.get('result', {})
            transactions = block.get('transactions', [])
            timestamp_hex = block.get('timestamp', '0x0')
            timestamp = int(timestamp_hex, 16)
            readable_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            transaction_details = []
            for transaction in transactions:
                transaction_detail = {
                    'Block Hash': transaction.get('blockHash'),
                    'Block Number': transaction.get('blockNumber'),
                    'From': transaction.get('from'),
                    'To': transaction.get('to'),
                    'Value': transaction.get('value'),
                    'Gas': transaction.get('gas'),
                    'Gas Price': transaction.get('gasPrice'),
                    'Timestamp': readable_time
                }
                transaction_details.append(transaction_detail)

            relevant_transactions = [
                tx for tx in transaction_details 
                if tx.get('To') and tx.get('To').lower() == wallet_address.lower()
            ]

            return relevant_transactions
    except Exception as e:
        current_app.logger.error(f"Exception occurred: {e}")
        return []

async def fetch_solana_transaction_data(session, wallet_address):
    try:
        async with session.post(Config.SOLANA_API_URL, json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getConfirmedSignaturesForAddress2",
            "params": [wallet_address]
        }) as response:
            response_json = await response.json()
            return response_json.get('result', [])
    except Exception as e:
        current_app.logger.error(f"Error fetching transactions: {e}")
        return []

def store_eth_transaction(transaction):
    try:
        conn = get_db_connection('eth_db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO eth_blockchain_transactions (transaction_hash, wallet_assets, token_names, value, timestamp, status, block_number, fee, transaction_index, input_data, signatures) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                transaction.get('hash'),
                "assets",
                "tokens",
                transaction.get('value', 0.0),
                transaction.get('Timestamp'),
                transaction.get('status', 'status'),
                transaction.get('blockNumber', 0),
                transaction.get('gas', 0.0),
                transaction.get('transactionIndex', 0),
                transaction.get('input', ''),
                "{}"
            )
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        current_app.logger.error(f"Error storing ETH transaction: {e}")

def store_solana_transaction(transaction):
    try:
        conn = get_db_connection('solana_db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO solana_blockchain_transactions (transaction_hash, wallet_assets, token_names, timestamp, block_number, fee, transaction_index, program_data, signatures) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                transaction.get('signature'),
                "assets",
                "tokens",
                transaction.get('Timestamp'),
                0,
                0.0,
                0,
                "program_data",
                "{}"
            )
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        current_app.logger.error(f"Error storing Solana transaction: {e}")

async def monitor_eth_wallet(wallet_address):
    async with aiohttp.ClientSession() as session:
        while True:
            transactions = await fetch_eth_transaction_data(session, wallet_address)
            for transaction in transactions:
                store_eth_transaction(transaction)
            await asyncio.sleep(10)

async def monitor_solana_wallet(wallet_address):
    async with aiohttp.ClientSession() as session:
        while True:
            transactions = await fetch_solana_transaction_data(session, wallet_address)
            for transaction in transactions:
                store_solana_transaction(transaction)
            await asyncio.sleep(10)

def monitor_eth(user_id, data):
    wallet_address = data.get('wallet_address')
    if not wallet_address:
        return jsonify({"error": "No wallet address provided"}), 400

    if not is_wallet_monitored(wallet_address, 'ethereum'):
        return jsonify({"error": "Wallet is not monitored"}), 400

    thread = threading.Thread(target=asyncio.run, args=(monitor_eth_wallet(wallet_address),))
    thread.start()
    return jsonify({"message": "ETH monitoring started"}), 201

def monitor_solana(user_id, data):
    wallet_address = data.get('wallet_address')
    if not wallet_address:
        return jsonify({"error": "No wallet address provided"}), 400

    if not is_wallet_monitored(wallet_address, 'solana'):
        return jsonify({"error": "Wallet is not monitored"}), 400

    thread = threading.Thread(target=asyncio.run, args=(monitor_solana_wallet(wallet_address),))
    thread.start()
    return jsonify({"message": "Solana monitoring started"}), 201
