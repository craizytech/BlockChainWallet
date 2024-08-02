from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.transactions.services import get_transactions
from app.transactions import transactions_bp

@transactions_bp.route('/get_transactions', methods=['POST'])
@jwt_required()
def get_transactions_route():
    data = request.get_json()
    wallet_address = data.get('wallet_address')
    network = data.get('network')

    if not wallet_address or not network:
        return jsonify({"error": "wallet_address and network are required"}), 400

    transactions = get_transactions(wallet_address, network)
    return transactions
