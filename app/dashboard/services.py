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

def create_dashboard(data):
    user_id = data.get('user_id')
    name = data.get('name')
    dashboard_type = data.get('type')
    
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO dashboards (user_id, name, type) VALUES (%s, %s, %s)",
            (user_id, name, dashboard_type)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Dashboard created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_dashboard(data):
    dashboard_id = data.get('dashboard_id')
    
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM dashboards WHERE id = %s",
            (dashboard_id,)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Dashboard deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_transactions(user_id):
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM transaction_data 
            WHERE wallet_id IN (
                SELECT id FROM monitored_wallets WHERE user_id = %s
            )
            """, 
            (user_id,)
        )
        transactions = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"transactions": transactions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
