import psycopg2
from psycopg2 import sql

# Database connection parameters
db_host = 'localhost'
db_user = 'postgres'
db_password = 'manu3326'
db_port = '5432'
db_name = 'blockchain_monitoring'

# SQL script to create the tables
create_tables_sql = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dashboards (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    network VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS wallets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    dashboard_id INTEGER REFERENCES dashboards(id) ON DELETE CASCADE,
    wallet_address VARCHAR(255) NOT NULL,
    network VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS monitored_wallets (
    id SERIAL PRIMARY KEY,
    wallet_id INTEGER REFERENCES wallets(id) ON DELETE CASCADE,
    network VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (wallet_id)
);

CREATE TABLE IF NOT EXISTS eth_transactions (
    id SERIAL PRIMARY KEY,
    wallet_id INTEGER REFERENCES monitored_wallets(wallet_id) ON DELETE CASCADE,
    block_hash VARCHAR(255) NOT NULL,
    block_number BIGINT NOT NULL,
    transaction_hash VARCHAR(255) NOT NULL UNIQUE,
    from_address VARCHAR(255) NOT NULL,
    to_address VARCHAR(255) NOT NULL,
    value DECIMAL(30, 8) NOT NULL,
    gas DECIMAL(30, 8) NOT NULL,
    gas_price DECIMAL(30, 8) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL
);

DROP INDEX IF EXISTS idx_eth_transaction_hash;
CREATE INDEX idx_eth_transaction_hash ON eth_transactions (transaction_hash);

CREATE TABLE IF NOT EXISTS solana_transactions (
    id SERIAL PRIMARY KEY,
    wallet_id INTEGER REFERENCES monitored_wallets(wallet_id) ON DELETE CASCADE,
    block_hash VARCHAR(255) NOT NULL,
    block_number BIGINT NOT NULL,
    transaction_hash VARCHAR(255) NOT NULL UNIQUE,
    from_address VARCHAR(255) NOT NULL,
    to_address VARCHAR(255) NOT NULL,
    value DECIMAL(30, 8) NOT NULL,
    gas DECIMAL(30, 8) NOT NULL,
    gas_price DECIMAL(30, 8) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL
);

DROP INDEX IF EXISTS idx_solana_transaction_hash;
CREATE INDEX idx_solana_transaction_hash ON solana_transactions (transaction_hash);
"""

# Connect to the default PostgreSQL database to create the new database
conn = psycopg2.connect(dbname='postgres', user=db_user, password=db_password, host=db_host, port=db_port)
conn.autocommit = True

# Create a cursor object
cur = conn.cursor()

try:
    # Drop the database if it exists
    cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_name)))
    # Create the new database
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    print(f"Database {db_name} created successfully.")
except psycopg2.errors.DuplicateDatabase:
    print(f"Database {db_name} already exists.")
except Exception as e:
    print(f"An error occurred: {e}")

# Close the cursor and connection to the default database
cur.close()
conn.close()

# Connect to the newly created database
db_conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
db_conn.autocommit = True

# Create a cursor object
db_cur = db_conn.cursor()

try:
    # Create tables
    db_cur.execute(create_tables_sql)
    print("Tables created successfully.")
except Exception as e:
    print(f"An error occurred while creating tables: {e}")

# Close the cursor and connection
db_cur.close()
db_conn.close()
