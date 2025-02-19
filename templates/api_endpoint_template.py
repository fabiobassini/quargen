"""
Questo file definisce un endpoint API aggiuntivo per il modulo {module_name}.
Scopo: Fornire funzionalità extra alle API esposte dal modulo.
Esempio di utilizzo:
    Se {prefix} è "extra", l'endpoint sarà accessibile all'indirizzo '/api/{module_name}/extra'.
"""

from flask import Blueprint, jsonify
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

api_endpoint_bp = Blueprint('{module_name}_{prefix}_endpoint', __name__, url_prefix='/api/{module_name}/{prefix}')

@api_endpoint_bp.route('/', methods=['GET'])
def endpoint_home():
    logger.info("Richiesta per l'endpoint {prefix}")
    return jsonify({{"message": "Risposta dall'endpoint {prefix}"}})

def get_endpoint():
    return api_endpoint_bp
