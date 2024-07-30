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

def add_wallet(user_id, dashboard_id, wallet_address, network):
    if not check_dashboard_exists(user_id, dashboard_id):
        return jsonify({"error": "Dashboard does not exist or does not belong to the user"}), 400
    
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
        return jsonify({"message": "Wallet added to dashboard successfully"}), 201
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
