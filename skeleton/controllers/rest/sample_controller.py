"""
Questo file definisce un controller REST per il modulo {MODULE_NAME}.
Scopo: Gestire richieste API REST e restituire risposte in formato JSON.
"""

from interfaces.business import IController
from flask import Blueprint, jsonify, request
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class SampleRestController(IController):
    def __init__(self):
        self.blueprint = Blueprint('{MODULE_NAME}_rest', __name__, url_prefix='/api/{MODULE_NAME}')
        self.register_routes()

    def register_routes(self):
        @self.blueprint.route('/sample', methods=['GET'])
        def sample():
            logger.info("Richiesta sample da SampleRestController")
            return jsonify({"message": "Risposta dal SampleRestController"})

    def get_blueprint(self):
        return self.blueprint

    def action(self):
        return "Azione eseguita da SampleRestController"
