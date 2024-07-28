from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.wallet.services import add_wallet, delete_wallet, get_wallets
from app.wallet import wallet_bp

@wallet_bp.route('/add', methods=['POST'])
@jwt_required()
def add():
    data = request.get_json()
    user_id = get_jwt_identity()
    return add_wallet(user_id, data)

@wallet_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
    data = request.get_json()
    user_id = get_jwt_identity()
    return delete_wallet(user_id, data)

@wallet_bp.route('/get', methods=['GET'])
@jwt_required()
def get():
    user_id = get_jwt_identity()
    return get_wallets(user_id)
