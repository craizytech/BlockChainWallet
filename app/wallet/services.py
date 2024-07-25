from flask import jsonify
from app.models.wallet import create_wallet as create_wallet_model, delete_wallet as delete_wallet_model

def create_wallet(data):
    user_id = data.get('user_id')
    wallet_address = data.get('wallet_address')
    network = data.get('network')
    
    create_wallet_model(user_id, wallet_address, network)
    return jsonify({"message": "Wallet created successfully"}), 201

def delete_wallet(data):
    wallet_id = data.get('wallet_id')
    
    delete_wallet_model(wallet_id)
    return jsonify({"message": "Wallet deleted successfully"}), 200
