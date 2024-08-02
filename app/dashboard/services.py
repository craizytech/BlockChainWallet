import psycopg2
from flask import jsonify
from app.config import Config
from datetime import datetime

def get_db_connection():
    conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )
    return conn

def create_dashboard(user_id, name, network_type, wallet_address):
    created_at = datetime.now()
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the wallet address already exists for the user
        cur.execute(
            "SELECT id FROM wallets WHERE user_id = %s AND wallet_address = %s",
            (user_id, wallet_address)
        )
        wallet = cur.fetchone()
        if wallet:
            return jsonify({"error": "Wallet address already exists in another dashboard"}), 409

        cur.execute(
            "INSERT INTO dashboards (user_id, name, network, wallet_address, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (user_id, name, network_type, wallet_address, created_at)
        )
        dashboard_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO wallets (user_id, dashboard_id, wallet_address, network, created_at) VALUES (%s, %s, %s, %s, %s)",
            (user_id, dashboard_id, wallet_address, network_type, created_at)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Dashboard created successfully", "dashboard_id": dashboard_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_dashboards(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, network, created_at, wallet_address FROM dashboards WHERE user_id = %s",
            (user_id,)
        )
        dashboards = cur.fetchall()
        cur.close()
        conn.close()
        dashboards_list = [
            {
                "id": dashboard[0],
                "name": dashboard[1],
                "network": dashboard[2],
                "created_at": dashboard[3],
                "wallet_address": dashboard[4]
            } for dashboard in dashboards
        ]
        return jsonify(dashboards_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_dashboard(user_id, dashboard_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Delete associated monitored wallets
        cur.execute(
            "DELETE FROM monitored_wallets WHERE wallet_id IN (SELECT id FROM wallets WHERE dashboard_id = %s)",
            (dashboard_id,)
        )

        # Delete associated wallets
        cur.execute(
            "DELETE FROM wallets WHERE dashboard_id = %s",
            (dashboard_id,)
        )

        # Delete the dashboard
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

def enable_monitoring(user_id, wallet_address, network):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Verify the wallet exists and belongs to the user
        cur.execute(
            "SELECT id FROM wallets WHERE user_id = %s AND wallet_address = %s AND network = %s",
            (user_id, wallet_address, network)
        )
        wallet = cur.fetchone()
        if not wallet:
            return jsonify({"error": "Wallet not found"}), 404

        wallet_id = wallet[0]

        # Check if the wallet is already being monitored
        cur.execute(
            "SELECT id FROM monitored_wallets WHERE wallet_id = %s",
            (wallet_id,)
        )
        if cur.fetchone():
            return jsonify({"error": "Wallet is already being monitored"}), 409

        # Add wallet to monitored_wallets
        cur.execute(
            "INSERT INTO monitored_wallets (wallet_id, network, created_at) VALUES (%s, %s, %s)",
            (wallet_id, network, datetime.now())
        )

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Monitoring enabled for wallet"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def disable_monitoring(user_id, wallet_address):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Verify the wallet exists and belongs to the user
        cur.execute(
            "SELECT id FROM wallets WHERE user_id = %s AND wallet_address = %s",
            (user_id, wallet_address)
        )
        wallet = cur.fetchone()
        if not wallet:
            return jsonify({"error": "Wallet not found"}), 404

        wallet_id = wallet[0]

        # Remove wallet from monitored_wallets
        cur.execute(
            "DELETE FROM monitored_wallets WHERE wallet_id = %s",
            (wallet_id,)
        )

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Monitoring disabled for wallet"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
