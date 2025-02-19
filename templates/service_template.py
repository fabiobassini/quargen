# templates/service_template.py
BUSINESS_SERVICE_TEMPLATE = '''"""
Questo file definisce un service di business per il modulo {module_name}.
Scopo: Implementare la logica di business dell'applicazione.
Utilizzo:
    - Il service espone un metodo "serve" che esegue una determinata logica di business.
Esempio:
    - Una chiamata a serve() restituirà "Risultato da SampleBusinessService".
"""

from interfaces.business import IService
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class SampleBusinessService(IService):
    def serve(self):
        # Esegue la logica di business
        logger.info("Esecuzione di SampleBusinessService")
        return "Risultato da SampleBusinessService"
'''
