"""
Questo file definisce un service di business per il modulo {MODULE_NAME}.
Scopo: Implementare la logica di business dell'applicazione.
"""

from interfaces.business import IService
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class SampleBusinessService(IService):
    def serve(self):
        logger.info("Esecuzione di SampleBusinessService")
        return "Risultato da SampleBusinessService"
