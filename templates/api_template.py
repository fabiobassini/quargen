# templates/api_template.py
API_TEMPLATE = '''"""
Questo file definisce il modulo API per il modulo {module_name}.
Scopo:
    - Esportare un insieme di endpoint REST per il modulo, che possono essere consumati da client esterni.
Utilizzo:
    - Crea un blueprint Flask con URL prefix '/api/{module_name}'.
    - Il metodo register_routes definisce un endpoint /status che restituisce lo stato dell'API.
Esempio:
    - Una richiesta GET a /api/{module_name}/status restituirà {"status": "API attiva"}.
    
Assicurati che il modulo implementi l'interfaccia IAPIModule per garantire coerenza e interoperabilità.
"""

from flask import Blueprint, jsonify
from interfaces.core import IAPIModule
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class APIModule(IAPIModule):
    def __init__(self):
        self.blueprint = Blueprint('{module_name}_api', __name__, url_prefix='/api/{module_name}')
        self.register_routes()

    def register_routes(self):
        @self.blueprint.route('/status')
        def status():
            logger.info("Richiesta status API")
            return jsonify({{"status": "API attiva"}})

    def get_api_blueprint(self):
        return self.blueprint

    def initialize(self, config: dict):
        logger.info("Inizializzo API con config: " + str(config))

    def start(self):
        logger.info("Avvio API")

    def stop(self):
        logger.info("Arresto API")

def initialize_api(config: dict):
    logger.info("Inizializzo l'API con config: " + str(config))
    return APIModule()
'''

