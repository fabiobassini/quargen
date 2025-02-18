from flask import Blueprint, jsonify
from utils.logger import ColoredLogger
logger = ColoredLogger(__name__).get_logger()

class APIModule:
    def __init__(self):
        self.blueprint = Blueprint('MyModule_api', __name__, url_prefix='/api/MyModule')
        self.register_routes()

    def register_routes(self):
        @self.blueprint.route('/status')
        def status():
            logger.info("Richiesta status API")
            return jsonify({"status": "API del modulo MyModule attiva"})

    def get_blueprint(self):
        return self.blueprint

def initialize_api(config: dict):
    logger.info("Inizializzo l'API di MyModule con config: " + str(config))
    return APIModule()
