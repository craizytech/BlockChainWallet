from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.transactions.services import send_eth, send_solana, get_transactions
from app.transactions import transactions_bp

@transactions_bp.route('/send_eth', methods=['POST'])
@jwt_required()
def send_eth_transaction():
    data = request.get_json()
    user_id = get_jwt_identity()
    return send_eth(user_id, data)

@transactions_bp.route('/send_solana', methods=['POST'])
@jwt_required()
def send_solana_transaction():
    data = request.get_json()
    user_id = get_jwt_identity()
    return send_solana(user_id, data)


@transactions_bp.route('/get_transactions', methods=['GET'])
@jwt_required()
def get_all_transactions():
    user_id = get_jwt_identity()
    wallet_address = request.args.get('wallet_address')
    return get_transactions(user_id, wallet_address)
