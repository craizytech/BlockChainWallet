import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    ETH_DB_URI = os.getenv('ETH_DB_URI', 'postgresql://postgres:password@localhost/eth_db')
    SOLANA_DB_URI = os.getenv('SOLANA_DB_URI', 'postgresql://postgres:password@localhost/solana_db')
    SYSTEM_DB_URI = os.getenv('SYSTEM_DB_URI', 'postgresql://postgres:password@localhost/system_db')
