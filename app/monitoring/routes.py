from flask import jsonify
from app.monitoring import monitoring_bp

@monitoring_bp.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'Monitoring running'})
