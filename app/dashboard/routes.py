from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dashboard.services import (
    create_dashboard,
    add_wallet,
    delete_dashboard,
    start_monitoring,
    stop_monitoring,
    get_dashboards
)
from app.dashboard import dashboard_bp

@dashboard_bp.route('/create_dashboard', methods=['POST'])
@jwt_required()
def create_dashboard_route():
    data = request.get_json()
    user_id = get_jwt_identity()
    return create_dashboard(user_id, data)

@dashboard_bp.route('/add_wallet', methods=['POST'])
@jwt_required()
def add_wallet_route():
    data = request.get_json()
    user_id = get_jwt_identity()
    return add_wallet(user_id, data)

@dashboard_bp.route('/delete_dashboard', methods=['DELETE'])
@jwt_required()
def delete_dashboard_route():
    data = request.get_json()
    user_id = get_jwt_identity()
    return delete_dashboard(user_id, data)

@dashboard_bp.route('/start_monitoring', methods=['POST'])
@jwt_required()
def start_monitoring_route():
    data = request.get_json()
    user_id = get_jwt_identity()
    return start_monitoring(user_id, data)

@dashboard_bp.route('/stop_monitoring', methods=['POST'])
@jwt_required()
def stop_monitoring_route():
    data = request.get_json()
    user_id = get_jwt_identity()
    return stop_monitoring(user_id, data)

@dashboard_bp.route('/get_dashboards', methods=['GET'])
@jwt_required()
def get_dashboards_route():
    user_id = get_jwt_identity()
    return get_dashboards(user_id)
