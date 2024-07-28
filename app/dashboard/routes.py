from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dashboard.services import create_dashboard, delete_dashboard
from app.dashboard import dashboard_bp

@dashboard_bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    user_id = get_jwt_identity()
    return create_dashboard(user_id, data)

@dashboard_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
    data = request.get_json()
    user_id = get_jwt_identity()
    return delete_dashboard(user_id, data)
