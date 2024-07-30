import psycopg2
from flask import jsonify
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

def create_dashboard(user_id, data):
    name = data.get('name')
    dashboard_type = data.get('type')
    
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO dashboards (user_id, name, type) VALUES (%s, %s, %s) RETURNING id",
            (user_id, name, dashboard_type)
        )
        dashboard_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Dashboard created successfully", "dashboard_id": dashboard_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def add_wallet(user_id, data):
    dashboard_id = data.get('dashboard_id')
    wallet_address = data.get('wallet_address')
    network = data.get('network')
    
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO monitored_wallets (user_id, dashboard_id, wallet_address, network) VALUES (%s, %s, %s, %s)",
            (user_id, dashboard_id, wallet_address, network)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Wallet added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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

def start_monitoring(user_id, data):
    dashboard_id = data.get('dashboard_id')
    
    # Assuming you have some function to start monitoring the wallet
    try:
        # Start monitoring logic here
        return jsonify({"message": "Monitoring started"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def stop_monitoring(user_id, data):
    dashboard_id = data.get('dashboard_id')
    
    # Assuming you have some function to stop monitoring the wallet
    try:
        # Stop monitoring logic here
        return jsonify({"message": "Monitoring stopped"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
