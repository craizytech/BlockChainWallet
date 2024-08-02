import requests
import asyncio
import time
import json

API_ENDPOINT = "https://api.devnet.solana.com"

async def get_latest_block():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getLatestBlockhash"
    }
    response = requests.post(API_ENDPOINT, json=payload)
    result = response.json()["result"]
    return result["value"]["blockhash"], result["context"]["slot"]

async def get_block_transactions(block_slot):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getConfirmedBlock",
        "params": [block_slot]
    }
    response = requests.post(API_ENDPOINT, json=payload)
    result = response.json()["result"]
    return result["transactions"]

async def get_transaction_details(signature):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getConfirmedTransaction",
        "params": [signature]
    }
    response = requests.post(API_ENDPOINT, json=payload)
    return response.json()["result"]

def convert_timestamp(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))

async def fetch_solana_transactions(wallet_address, db_conn):
    latest_block_hash, latest_block_slot = await get_latest_block()
    
    transactions_list = []
    for slot in range(latest_block_slot, latest_block_slot - 5, -1):
        transactions = await get_block_transactions(slot)

        for transaction in transactions:
            signature = transaction["transaction"]["signatures"][0]
            transaction_details = await get_transaction_details(signature)

            if transaction_details:
                transaction_hash = signature
                from_address = transaction_details["transaction"]["message"]["accountKeys"][0]
                to_address = transaction_details["transaction"]["message"]["accountKeys"][1]
                value = transaction_details["meta"]["postBalances"][1] - transaction_details["meta"]["preBalances"][1]
                gas = transaction_details["meta"]["fee"]
                gas_price = 0  # Solana does not have a gas price like Ethereum
                timestamp = convert_timestamp(transaction_details["blockTime"])

                if from_address == wallet_address or to_address == wallet_address:
                    transaction_data = {
                        'block_hash': latest_block_hash,
                        'block_number': slot,
                        'transaction_hash': transaction_hash,
                        'from_address': from_address,
                        'to_address': to_address,
                        'value': value,
                        'gas': gas,
                        'gas_price': gas_price,
                        'timestamp': timestamp
                    }
                    transactions_list.append(transaction_data)
                    
                    cur = db_conn.cursor()
                    cur.execute(
                        "INSERT INTO solana_transactions (block_hash, block_number, transaction_hash, from_address, to_address, value, gas, gas_price, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                        (transaction_data['block_hash'], transaction_data['block_number'], transaction_data['transaction_hash'], transaction_data['from_address'], transaction_data['to_address'], transaction_data['value'], transaction_data['gas'], transaction_data['gas_price'], transaction_data['timestamp'])
                    )
                    db_conn.commit()
                    cur.close()
                    
    return transactions_list

async def monitor_solana_wallet(wallet_address, db_conn):
    while True:
        transactions = await fetch_solana_transactions(wallet_address, db_conn)
        if transactions:
            print(json.dumps(transactions, indent=4))
        else:
            print(f"No transactions found for wallet {wallet_address}.")
        await asyncio.sleep(30)  # Check every 30 seconds
