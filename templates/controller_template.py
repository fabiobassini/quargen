# templates/controller_template.py
REST_CONTROLLER_TEMPLATE = '''from interfaces.business import IController
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
