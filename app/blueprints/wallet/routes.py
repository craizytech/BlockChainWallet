from flask import Blueprint, request, jsonify
from app.blueprints.wallet.services import create_wallet, delete_wallet

wallet_bp = Blueprint('wallet', __name__, url_prefix='/wallet')

@wallet_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    return create_wallet(data)

@wallet_bp.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    return delete_wallet(data)
