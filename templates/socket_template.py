# templates/socket_template.py
SOCKET_TEMPLATE = '''from interfaces.core import ISocketModule
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class SocketModule(ISocketModule):
    def __init__(self):
        pass

    def handle_connection(self, connection):
        logger.info("Gestisco la connessione nel modulo {module_name}: " + str(connection))

    def initialize(self, config: dict):
        logger.info("Inizializzo il modulo sockets con config: " + str(config))

    def start(self):
        logger.info("Avvio modulo sockets")

    def stop(self):
        logger.info("Arresto modulo sockets")

def initialize_socket(config: dict):
    logger.info("Inizializzo il modulo sockets con config: " + str(config))
    return SocketModule()
'''
