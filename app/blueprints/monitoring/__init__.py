from flask import Blueprint

monitoring_bp = Blueprint('monitoring', __name__)

from . import eth_monitor, solana_monitor, routes
