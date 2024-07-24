import psycopg2
from psycopg2 import sql

# Database connection parameters
db_host = 'localhost'
db_user = 'your_db_user'
db_password = 'your_db_password'
db_port = '5432'

# Database names
databases = {
    'eth_db': """
        CREATE TABLE IF NOT EXISTS wallets (
            id SERIAL PRIMARY KEY,
            wallet_address VARCHAR(255) NOT NULL UNIQUE,
            wallet_name VARCHAR(255)
        );

        CREATE TABLE IF NOT EXISTS eth_blockchain_transactions (
            id SERIAL PRIMARY KEY,
            transaction_hash VARCHAR(255) NOT NULL UNIQUE,
            wallet_assets VARCHAR(255),
            token_names VARCHAR(255),
            value DECIMAL(20, 8),
            timestamp TIMESTAMPTZ NOT NULL,
            status VARCHAR(50),
            block_number BIGINT,
            fee DECIMAL(20, 8),
            transaction_index INTEGER,
            input_data TEXT,
            signatures JSONB
        );

        CREATE TABLE IF NOT EXISTS transaction_inputs (
            id SERIAL PRIMARY KEY,
            transaction_id INTEGER REFERENCES eth_blockchain_transactions(id) ON DELETE CASCADE,
            sender_wallet_id INTEGER REFERENCES wallets(id) ON DELETE CASCADE,
            amount_sent DECIMAL(20, 8)
        );

        CREATE TABLE IF NOT EXISTS transaction_outputs (
            id SERIAL PRIMARY KEY,
            transaction_id INTEGER REFERENCES eth_blockchain_transactions(id) ON DELETE CASCADE,
            recipient_wallet_id INTEGER REFERENCES wallets(id) ON DELETE CASCADE,
            amount_received DECIMAL(20, 8)
        );
    """,
    'solana_db': """
        CREATE TABLE IF NOT EXISTS solana_wallets (
            id SERIAL PRIMARY KEY,
            wallet_address VARCHAR(255) NOT NULL UNIQUE,
            wallet_name VARCHAR(255)
        );

        CREATE TABLE IF NOT EXISTS solana_blockchain_transactions (
            id SERIAL PRIMARY KEY,
            transaction_hash VARCHAR(255) NOT NULL UNIQUE,
            wallet_assets VARCHAR(255),
            token_names VARCHAR(255),
            timestamp TIMESTAMPTZ NOT NULL,
            block_number BIGINT,
            fee DECIMAL(20, 8),
            transaction_index INTEGER,
            program_data TEXT,
            signatures JSONB
        );

        CREATE TABLE IF NOT EXISTS solana_transaction_inputs (
            id SERIAL PRIMARY KEY,
            transaction_id INTEGER REFERENCES solana_blockchain_transactions(id) ON DELETE CASCADE,
            sender_wallet_id INTEGER REFERENCES solana_wallets(id) ON DELETE CASCADE,
            amount_sent DECIMAL(20, 8)
        );

        CREATE TABLE IF NOT EXISTS solana_transaction_outputs (
            id SERIAL PRIMARY KEY,
            transaction_id INTEGER REFERENCES solana_blockchain_transactions(id) ON DELETE CASCADE,
            recipient_wallet_id INTEGER REFERENCES solana_wallets(id) ON DELETE CASCADE,
            amount_received DECIMAL(20, 8)
        );
    """,
    'system_db': """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS dashboards (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            name VARCHAR(255) NOT NULL,
            type VARCHAR(50) NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS monitored_wallets (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            wallet_address VARCHAR(255) NOT NULL,
            network VARCHAR(50) NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS transaction_data (
            id SERIAL PRIMARY KEY,
            wallet_id INTEGER REFERENCES monitored_wallets(id) ON DELETE CASCADE,
            transaction_hash VARCHAR(255) NOT NULL,
            value DECIMAL(20, 8),
            timestamp TIMESTAMPTZ NOT NULL,
            status VARCHAR(50),
            block_number BIGINT,
            fee DECIMAL(20, 8),
            transaction_index INTEGER,
            network VARCHAR(50) NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """
}

# Connect to the default PostgreSQL database
conn = psycopg2.connect(dbname='postgres', user=db_user, password=db_password, host=db_host, port=db_port)
conn.autocommit = True

# Create a cursor object
cur = conn.cursor()

# Create databases
for db, create_table_query in databases.items():
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db)))
    conn.close()  # Close connection to default 'postgres' database

    # Connect to the new database
    conn = psycopg2.connect(dbname=db, user=db_user, password=db_password, host=db_host, port=db_port)
    conn.autocommit = True
    cur = conn.cursor()

    # Create tables
    cur.execute(create_table_query)

    # Close the cursor and connection
    cur.close()
    conn.close()

print("Databases and tables created successfully.")
