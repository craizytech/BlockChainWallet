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
    type = data.get('type')
    
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO dashboards (user_id, name, type) VALUES (%s, %s, %s)",
            (user_id, name, type)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Dashboard created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_dashboard(user_id, data):
    dashboard_id = data.get('dashboard_id')
    
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM dashboards WHERE id = %s AND user_id = %s",
            (dashboard_id, user_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Dashboard deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_dashboard(user_id):
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM dashboards WHERE user_id = %s", (user_id,))
        dashboards = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"dashboards": dashboards}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
