"""
Questo file definisce il modulo UI per il modulo configurato.
Scopo: Gestire il rendering della parte front-end dell'applicazione.
Utilizzo:
    - Crea un blueprint Flask per la UI.
    - Registra le rotte per la pagina index e eventuali endpoint extra.
Esempio:
    - Una richiesta GET a "/" renderizzerà il template "index/index.html".
"""

from flask import Blueprint, render_template
import os
import importlib
from interfaces.core import IUIComponent
from utils.logger import ColoredLogger
from ..config.default import CONFIG  # Import relativo corretto

logger = ColoredLogger(__name__).get_logger()

class UIModule(IUIComponent):
    def __init__(self):
        self.blueprint = Blueprint(CONFIG["module_name"] + "_ui", __name__, url_prefix='/',
                                     template_folder='templates', static_folder='static', static_url_path='/static')
        self.register_routes()
        self.register_extra_endpoints()

    def register_routes(self):
        @self.blueprint.route('/')
        def home():
            logger.info("Richiesta pagina index")
            return render_template('index/index.html', module=CONFIG["module_name"])

    def register_extra_endpoints(self):
        module_name = CONFIG.get("module_name", "")
        endpoints_dir = os.path.join(os.path.dirname(__file__), 'endpoints')
        if os.path.exists(endpoints_dir):
            for filename in os.listdir(endpoints_dir):
                if filename.endswith('_endpoint.py'):
                    mod_name = filename[:-3]
                    try:
                        mod = importlib.import_module(f"{module_name}.ui.endpoints.{mod_name}")
                        if hasattr(mod, 'register_endpoint'):
                            mod.register_endpoint(self.blueprint)
                            logger.info("Registrato endpoint da " + filename)
                    except Exception as e:
                        logger.error("Errore nel registrare endpoint da {}: {}".format(filename, e))

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
