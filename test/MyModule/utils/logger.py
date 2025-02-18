import logging

class ColoredLogger:
    COLORS = {
        'DEBUG': '\033[94m',     # Blu
        'INFO': '\033[92m',      # Verde
        'WARNING': '\033[93m',   # Giallo
        'ERROR': '\033[91m',     # Rosso
        'CRITICAL': '\033[95m'   # Magenta
    }
    RESET = '\033[0m'

    class ColoredFormatter(logging.Formatter):
        def format(self, record):
            levelname = record.levelname
            if levelname in ColoredLogger.COLORS:
                record.levelname = "{}{}{}".format(ColoredLogger.COLORS[levelname], levelname, ColoredLogger.RESET)
            return super().format(record)

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setFormatter(self.ColoredFormatter('[%(levelname)s] %(message)s'))
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger
