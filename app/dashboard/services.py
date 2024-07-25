from flask import jsonify
from app.models.dashboard import create_dashboard as create_dashboard_model, delete_dashboard as delete_dashboard_model, get_transactions

def create_dashboard(data):
    user_id = data.get('user_id')
    name = data.get('name')
    type = data.get('type')
    
    create_dashboard_model(user_id, name, type)
    return jsonify({"message": "Dashboard created successfully"}), 201

def delete_dashboard(data):
    dashboard_id = data.get('dashboard_id')
    
    delete_dashboard_model(dashboard_id)
    return jsonify({"message": "Dashboard deleted successfully"}), 200

def show_transactions(wallet_id, network):
    transactions = get_transactions(wallet_id, network)
    return jsonify({"transactions": transactions}), 200
