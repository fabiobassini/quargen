# templates/controller_template.py
REST_CONTROLLER_TEMPLATE = '''"""
Questo file definisce un controller REST per il modulo {module_name}.
Scopo: Gestire richieste API REST e restituire risposte in formato JSON.
Utilizzo:
    - Il controller crea un blueprint Flask con un endpoint (es. /api/{module_name}/sample).
Esempio:
    - Una richiesta GET a /api/{module_name}/sample attiverà il metodo sample e restituirà una risposta JSON.
"""

from interfaces.business import IController
from flask import Blueprint, request, jsonify
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class SampleRestController(IController):
    def __init__(self):
        self.blueprint = Blueprint('{module_name}_rest', __name__, url_prefix='/api/{module_name}')
        self.register_routes()

    def register_routes(self):
        @self.blueprint.route('/sample', methods=['GET'])
        def sample():
            logger.info("Richiesta sample da SampleRestController")
            return jsonify({{"message": "Risposta dal SampleRestController"}})

    def get_blueprint(self):
        return self.blueprint

    def action(self):
        # Esegui la logica del controller
        return "Azione eseguita da SampleRestController"
'''
