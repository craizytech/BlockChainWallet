from flask import request, jsonify
from app.dashboard.services import create_dashboard, delete_dashboard, get_transactions
from app.dashboard import dashboard_bp

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
    user_id = request.args.get('user_id')
    return get_transactions(user_id)
