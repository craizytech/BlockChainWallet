import asyncio
from app.blueprints.monitoring.eth_monitor import monitor_ethereum
from app.blueprints.monitoring.solana_monitor import monitor_solana

async def main():
    await asyncio.gather(
        monitor_ethereum(),
        monitor_solana()
    )

if __name__ == "__main__":
    asyncio.run(main())
