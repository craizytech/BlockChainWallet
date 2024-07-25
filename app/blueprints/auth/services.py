import bcrypt
from flask import jsonify
from app.models.user import create_user, get_user_by_email
from app.blueprints.auth.utils import create_jwt_token

def register_user(data):
    email = data.get('email')
    password = data.get('password')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    create_user(email, hashed_password)
    return jsonify({"message": "User registered successfully"}), 201

def login_user(data):
    email = data.get('email')
    password = data.get('password')
    user = get_user_by_email(email)
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        token = create_jwt_token(user['id'])
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
