from flask import Blueprint, render_template
import os, importlib
from utils.logger import ColoredLogger
logger = ColoredLogger(__name__).get_logger()

class UIModule:
    def __init__(self):
        self.blueprint = Blueprint('MyModule_ui', __name__, url_prefix='/', 
                                     template_folder='templates', static_folder='static', static_url_path='/static')
        self.register_routes()
        self.register_extra_endpoints()

    def register_routes(self):
        @self.blueprint.route('/')
        def home():
            logger.info("Richiesta pagina index")
            return render_template('index/index.html', module="MyModule")

    def register_extra_endpoints(self):
        endpoints_dir = os.path.join(os.path.dirname(__file__), 'endpoints')
        if os.path.exists(endpoints_dir):
            for filename in os.listdir(endpoints_dir):
                if filename.endswith('_endpoint.py'):
                    mod_name = filename[:-3]
                    mod = importlib.import_module('ui.endpoints.' + mod_name)
                    if hasattr(mod, 'register_endpoint'):
                        mod.register_endpoint(self.blueprint)
                        logger.info("Registrato endpoint da {filename}")
                        
    def get_blueprint(self):
        return self.blueprint

def initialize_ui(config: dict):
    logger.info("Inizializzo la UI di MyModule con config: " + str(config))
    return UIModule()
