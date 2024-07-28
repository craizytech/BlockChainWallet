from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.monitoring.services import monitor_eth, monitor_solana
from app.monitoring import monitoring_bp

@monitoring_bp.route('/eth', methods=['POST'])
@jwt_required()
def eth():
    data = request.get_json()
    user_id = get_jwt_identity()
    return monitor_eth(user_id, data)

@monitoring_bp.route('/solana', methods=['POST'])
@jwt_required()
def solana():
    data = request.get_json()
    user_id = get_jwt_identity()
    return monitor_solana(user_id, data)
