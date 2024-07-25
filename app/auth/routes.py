from flask import request, jsonify
from app.auth.services import register_user, login_user
from app.auth import auth_bp

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)
