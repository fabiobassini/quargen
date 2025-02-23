"""
Modulo API per il modulo {MODULE_NAME}.
Scopo: Esporre endpoint REST per il modulo.
"""

from flask import Blueprint, jsonify
from interfaces.core import IAPIModule
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class APIModule(IAPIModule):
    def __init__(self):
        self.blueprint = Blueprint('{MODULE_NAME}_api', __name__, url_prefix='/api/{MODULE_NAME}')
        self.register_routes()

    def register_routes(self):
        @self.blueprint.route('/status', methods=['GET'])
        def status():
            logger.info("Richiesta status API")
            return jsonify({"status": "API attiva"})

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
