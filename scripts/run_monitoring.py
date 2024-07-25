import threading
import asyncio
from app.monitoring.eth_monitor import start_eth_monitoring
from app.monitoring.solana_monitor import start_solana_monitoring

def run_eth_monitoring():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_eth_monitoring())

def run_solana_monitoring():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_solana_monitoring())

if __name__ == "__main__":
    eth_thread = threading.Thread(target=run_eth_monitoring)
    solana_thread = threading.Thread(target=run_solana_monitoring)

    eth_thread.start()
    solana_thread.start()

    eth_thread.join()
    solana_thread.join()
