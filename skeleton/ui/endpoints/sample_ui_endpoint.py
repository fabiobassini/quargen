"""
Endpoint extra per la UI del modulo {MODULE_NAME}.
Scopo: Aggiungere funzionalità extra per il rendering della UI.
"""

from flask import Blueprint, render_template
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

# Blueprint registrata con URL prefix "/sample" per il sample UI endpoint
sample_ui_ep = Blueprint("{MODULE_NAME}_ui_ep", __name__, url_prefix="/sample")

@sample_ui_ep.route("/", methods=["GET"])
def sample_endpoint():
    logger.info("Richiesta per endpoint UI extra")
    return render_template("index/index.html")

"""
Endpoint extra per la UI del modulo MyApp.
Scopo: Aggiungere funzionalità extra per il rendering della UI.
"""

from flask import Blueprint, render_template
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

# Blueprint registrato con URL prefix "/sample" per il sample UI endpoint
sample_ui_ep = Blueprint("MyApp_ui_ep", __name__, url_prefix="/sample")

@sample_ui_ep.route("/", methods=["GET"])
def sample_endpoint():
    logger.info("Richiesta per endpoint UI extra")
    return render_template("index/index.html")

def register_endpoint(parent_bp):
    """
    Registra il blueprint dell'endpoint extra all'interno del blueprint principale della UI.
    """
    parent_bp.register_blueprint(sample_ui_ep)
