import psycopg2
import asyncio
import threading
from app.config import Config
from app.monitoring.eth_monitor import monitor_eth_wallet
from app.monitoring.solana_monitor import monitor_solana_wallet

def get_db_connection():
    conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )
    return conn

def get_monitored_wallets():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT wallet_address, network FROM monitored_wallets")
    wallets = cur.fetchall()
    cur.close()
    conn.close()
    return wallets

async def start_monitoring():
    monitored_wallets = get_monitored_wallets()
    db_conn = get_db_connection()

    for wallet_address, network in monitored_wallets:
        if network.lower() == 'ethereum':
            asyncio.create_task(monitor_eth_wallet(wallet_address, db_conn))
        elif network.lower() == 'solana':
            asyncio.create_task(monitor_solana_wallet(wallet_address, db_conn))
        else:
            print(f"Unknown network: {network}")

def run_monitoring():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_monitoring())

def start_monitoring_engine():
    monitoring_thread = threading.Thread(target=run_monitoring)
    monitoring_thread.start()
