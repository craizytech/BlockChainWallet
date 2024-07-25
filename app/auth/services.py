import psycopg2
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
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

def register_user(data):
    email = data.get('email')
    password = data.get('password')
    hashed_password = generate_password_hash(password)
    
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            (email, hashed_password)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def login_user(data):
    email = data.get('email')
    password = data.get('password')
    
    try:
        conn = get_db_connection('system_db')
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user and check_password_hash(user[0], password):
            access_token = create_access_token(identity=email)
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400
