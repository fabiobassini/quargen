"""
Endpoint extra per la UI del modulo {MODULE_NAME}.
Scopo: Aggiungere funzionalità extra per il rendering della UI.
"""

from flask import Blueprint, render_template
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

sample_ui_ep = Blueprint('{MODULE_NAME}_ui_ep', __name__, url_prefix='/ui/{MODULE_NAME}')

@sample_ui_ep.route('/', methods=['GET'])
def sample_endpoint():
    logger.info("Richiesta per endpoint UI extra")
    return render_template("index/index.html")
