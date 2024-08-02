import requests
import json
import asyncio
from datetime import datetime
from app.config import Config

# Ethereum endpoint URL
ETH_URL = Config.ETH_API_URL

async def get_block(block_number):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True],
        "id": 1,
    }
    response = requests.post(ETH_URL, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Received status code {response.status_code}")
        return None

async def get_latest_block_number():
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1,
    }
    response = requests.post(ETH_URL, json=payload)
    if response.status_code == 200:
        return int(response.json()["result"], 16)
    else:
        print(f"Error: Received status code {response.status_code}")
        return None

async def fetch_transactions(wallet_address):
    latest_block_number = await get_latest_block_number()
    if latest_block_number is None:
        return []

    transactions_list = []
    for block_number in range(latest_block_number, latest_block_number - 5, -1):
        block_data = await get_block(block_number)
        if block_data:
            try:
                transactions = block_data["result"]["transactions"]
                timestamp = block_data["result"]["timestamp"]
                readable_time = datetime.utcfromtimestamp(int(timestamp, 16)).strftime('%Y-%m-%d %H:%M:%S')
                filtered_transactions = [
                    {
                        'block_hash': tx.get('blockHash'),
                        'block_number': tx.get('blockNumber'),
                        'transaction_hash': tx.get('hash'),
                        'from_address': tx.get('from'),
                        'to_address': tx.get('to'),
                        'value': tx.get('value'),
                        'gas': tx.get('gas'),
                        'gas_price': tx.get('gasPrice'),
                        'timestamp': readable_time
                    }
                    for tx in transactions if tx["from"] == wallet_address or tx["to"] == wallet_address
                ]
                transactions_list.extend(filtered_transactions)
            except KeyError:
                print("Error: Unexpected JSON response structure")
    return transactions_list

async def monitor_eth_wallet(wallet_address, db_conn):
    while True:
        transactions = await fetch_transactions(wallet_address)
        if transactions:
            print(json.dumps(transactions, indent=4))
            # code to insert data into the table
            cur = db_conn.cursor()
            for tx in transactions:
                cur.execute(
                    "INSERT INTO eth_transactions (block_hash, block_number, transaction_hash, from_address, to_address, value, gas, gas_price, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                    (tx['block_hash'], tx['block_number'], tx['transaction_hash'], tx['from_address'], tx['to_address'], tx['value'], tx['gas'], tx['gas_price'], tx['timestamp'])
                )
            db_conn.commit()
            cur.close()
        else:
            print(f"No transactions found for wallet {wallet_address} in the last 5 blocks.")
        await asyncio.sleep(30)  # Check every 30 seconds
