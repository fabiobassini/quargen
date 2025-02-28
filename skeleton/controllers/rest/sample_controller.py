from interfaces.business import IController
from flask import Blueprint, jsonify, request
from utils.logger import ColoredLogger
from ...config.default import CONFIG  # <== Modifica qui: usa tre punti per risalire a MyApp/config

logger = ColoredLogger(__name__).get_logger()

class SampleRestController(IController):
    def __init__(self):
        # Crea il blueprint con il prefisso fisso preso dal CONFIG
        self.blueprint = Blueprint("{MODULE_NAME}_controller", __name__, url_prefix=CONFIG["controller_blueprint_prefix"])
        self.register_routes()

    def register_routes(self):
        # La route custom viene presa dalla configurazione (oppure può essere sostituita dinamicamente tramite CLI)
        @self.blueprint.route(CONFIG["sample_controller_route"], methods=["GET"])
        def sample():
            logger.info("Richiesta sample da SampleRestController")
            return jsonify({"message": "Risposta dal SampleRestController"})

    def get_blueprint(self):
        return self.blueprint

    def action(self):
        return "Azione eseguita da SampleRestController"
