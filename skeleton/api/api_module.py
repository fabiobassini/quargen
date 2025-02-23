from flask import Blueprint, jsonify
from interfaces.core import IAPIModule
from utils.logger import ColoredLogger
from ..config.default import CONFIG

logger = ColoredLogger(__name__).get_logger()

class APIModule(IAPIModule):
    def __init__(self):
        # Usa il prefisso fisso definito in CONFIG
        self.blueprint = Blueprint("{MODULE_NAME}_api", __name__, url_prefix=CONFIG["api_blueprint_prefix"])
        self.register_routes()

    def register_routes(self):
        @self.blueprint.route("/status", methods=["GET"])
        def status():
            logger.info("Richiesta status API")
            return jsonify({"status": "API attiva"})

    def get_api_blueprint(self):
        return self.blueprint

    def initialize(self, config: dict):
        logger.info("Inizializzo l'API con config: " + str(config))

    def start(self):
        logger.info("Avvio API")

    def stop(self):
        logger.info("Arresto API")

def initialize_api(config: dict):
    logger.info("Inizializzo l'API con config: " + str(config))
    return APIModule()
