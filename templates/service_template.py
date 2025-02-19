# templates/service_template.py
BUSINESS_SERVICE_TEMPLATE = '''from interfaces.business import IService
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class SampleBusinessService(IService):
    def serve(self):
        # Esegue la logica di business
        logger.info("Esecuzione di SampleBusinessService")
        return "Risultato da SampleBusinessService"
'''
