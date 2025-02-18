from utils.logger import ColoredLogger
logger = ColoredLogger(__name__).get_logger()

class SocketModule:
    def __init__(self):
        pass

    def handle_connection(self, connection):
        logger.info("Gestisco la connessione nel modulo MyModule: " + str(connection))

def initialize_socket(config: dict):
    logger.info("Inizializzo il modulo sockets di MyModule con config: " + str(config))
    return SocketModule()
