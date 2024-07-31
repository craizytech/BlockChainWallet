import psycopg2
from flask import jsonify, current_app
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

def create_dashboard_and_add_wallet(user_id, data):
    name = data.get('name')
    network = data.get('network')
    wallet_address = data.get('wallet_address')
    
    if not name or not network or not wallet_address:
        return jsonify({"error": "Name, network, and wallet address are required"}), 400

    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO dashboards (user_id, name, type) VALUES (%s, %s, %s) RETURNING id",
            (user_id, name, network)
        )
        dashboard_id = cur.fetchone()[0]
        
        cur.execute(
            "INSERT INTO monitored_wallets (user_id, dashboard_id, wallet_address, network) VALUES (%s, %s, %s, %s)",
            (user_id, dashboard_id, wallet_address, network)
        )
        
        conn.commit()
        cur.close()
        conn.close()

        if network.lower() == 'solana':
            add_wallet_to_network('solana_db', wallet_address)
        elif network.lower() == 'ethereum':
            add_wallet_to_network('eth_db', wallet_address)
        
        return jsonify({"message": "Dashboard and wallet created successfully", "dashboard_id": dashboard_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def add_wallet_to_network(db_name, wallet_address):
    try:
        conn = get_db_connection(db_name)
        cur = conn.cursor()
        if db_name == 'solana_db':
            cur.execute(
                "INSERT INTO solana_wallets (wallet_address) VALUES (%s) ON CONFLICT (wallet_address) DO NOTHING",
                (wallet_address,)
            )
        elif db_name == 'eth_db':
            cur.execute(
                "INSERT INTO eth_wallets (wallet_address) VALUES (%s) ON CONFLICT (wallet_address) DO NOTHING",
                (wallet_address,)
            )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        current_app.logger.error(f"Error adding wallet to {db_name}: {e}")
        raise

def check_dashboard_exists(user_id, dashboard_id):
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute("SELECT id FROM dashboards WHERE id = %s AND user_id = %s", (dashboard_id, user_id))
        dashboard = cur.fetchone()
        cur.close()
        conn.close()
        return dashboard is not None
    except Exception as e:
        return False

def delete_dashboard(user_id, data):
    dashboard_id = data.get('dashboard_id')
    
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute("DELETE FROM dashboards WHERE id = %s AND user_id = %s", (dashboard_id, user_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Dashboard deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_dashboards(user_id):
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                d.id, d.name, d.type, mw.wallet_address, mw.network
            FROM 
                dashboards d
            LEFT JOIN 
                monitored_wallets mw ON d.id = mw.dashboard_id
            WHERE 
                d.user_id = %s
        """, (user_id,))
        dashboards = cur.fetchall()
        cur.close()
        conn.close()
        
        dashboards_list = []
        for dashboard in dashboards:
            dashboards_list.append({
                "dashboard_id": dashboard[0],
                "name": dashboard[1],
                "type": dashboard[2],
                "wallet_address": dashboard[3],
                "network": dashboard[4]
            })
        
        return jsonify({"dashboards": dashboards_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
