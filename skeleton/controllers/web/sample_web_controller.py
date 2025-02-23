"""
Questo file definisce un controller web per il modulo {MODULE_NAME}.
Scopo: Renderizzare template HTML per la UI.
"""

from interfaces.business import IController
from flask import render_template
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class SampleWebController(IController):
    def action(self):
        return render_template("index/index.html")
