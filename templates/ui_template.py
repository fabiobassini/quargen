# templates/ui_template.py
UI_TEMPLATE = '''from flask import Blueprint, render_template
import os, importlib
from interfaces.core import IUIComponent
from utils.logger import ColoredLogger
logger = ColoredLogger(__name__).get_logger()

class UIModule(IUIComponent):
    def __init__(self):
        self.blueprint = Blueprint('{module_name}_ui', __name__, url_prefix='/', 
                                     template_folder='templates', static_folder='static', static_url_path='/static')
        self.register_routes()
        self.register_extra_endpoints()

    def register_routes(self):
        @self.blueprint.route('/')
        def home():
            logger.info("Richiesta pagina index")
            return render_template('index/index.html', module="{module_name}")

    def register_extra_endpoints(self):
        endpoints_dir = os.path.join(os.path.dirname(__file__), 'endpoints')
        if os.path.exists(endpoints_dir):
            for filename in os.listdir(endpoints_dir):
                if filename.endswith('_endpoint.py'):
                    mod_name = filename[:-3]
                    mod = importlib.import_module('{module_name}.ui.endpoints.' + mod_name)
                    if hasattr(mod, 'register_endpoint'):
                        mod.register_endpoint(self.blueprint)
                        logger.info("Registrato endpoint da " + filename)

    def get_ui_blueprint(self):
        return self.blueprint

    def initialize(self, config: dict):
        logger.info("Inizializzo la UI con config: " + str(config))

    def start(self):
        logger.info("Avvio UI")

    def stop(self):
        logger.info("Arresto UI")

def initialize_ui(config: dict):
    logger.info("Inizializzo la UI con config: " + str(config))
    return UIModule()
'''
