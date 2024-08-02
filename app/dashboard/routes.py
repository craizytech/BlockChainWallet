from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dashboard.services import create_dashboard, get_dashboards, delete_dashboard, enable_monitoring, disable_monitoring
from app.dashboard import dashboard_bp

@dashboard_bp.route('/create_dashboard', methods=['POST'])
@jwt_required()
def create_dashboard_route():
    user_id = get_jwt_identity()
    data = request.get_json()
    name = data.get('name')
    network_type = data.get('network_type')
    wallet_address = data.get('wallet_address')
    return create_dashboard(user_id, name, network_type, wallet_address)

@dashboard_bp.route('/get_dashboards', methods=['GET'])
@jwt_required()
def get_dashboards_route():
    user_id = get_jwt_identity()
    return get_dashboards(user_id)

@dashboard_bp.route('/delete_dashboard', methods=['DELETE'])
@jwt_required()
def delete_dashboard_route():
    user_id = get_jwt_identity()
    data = request.get_json()
    dashboard_id = data.get('dashboard_id')
    return delete_dashboard(user_id, dashboard_id)

@dashboard_bp.route('/enable_monitoring', methods=['POST'])
@jwt_required()
def enable_monitoring_route():
    user_id = get_jwt_identity()
    data = request.get_json()
    wallet_address = data.get('wallet_address')
    network = data.get('network')
    return enable_monitoring(user_id, wallet_address, network)

@dashboard_bp.route('/disable_monitoring', methods=['POST'])
@jwt_required()
def disable_monitoring_route():
    user_id = get_jwt_identity()
    data = request.get_json()
    wallet_address = data.get('wallet_address')
    return disable_monitoring(user_id, wallet_address)
