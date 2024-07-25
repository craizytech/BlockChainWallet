from flask import Blueprint, request, jsonify
from app.blueprints.dashboard.services import create_dashboard, delete_dashboard, show_transactions

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    return create_dashboard(data)

@dashboard_bp.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    return delete_dashboard(data)

@dashboard_bp.route('/transactions', methods=['GET'])
def transactions():
    wallet_id = request.args.get('wallet_id')
    network = request.args.get('network')
    return show_transactions(wallet_id, network)
