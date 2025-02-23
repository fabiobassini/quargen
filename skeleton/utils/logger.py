"""
Logger generico con output colorato.
"""

import logging

class ColoredLogger:
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[95m'
    }
    RESET = '\033[0m'

    class ColoredFormatter(logging.Formatter):
        def format(self, record):
            level = record.levelname
            if level in ColoredLogger.COLORS:
                record.levelname = f"{ColoredLogger.COLORS[level]}{level}{ColoredLogger.RESET}"
            return super().format(record)

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setFormatter(self.ColoredFormatter('[%(levelname)s] %(message)s'))
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger

if __name__ == '__main__':
    logger = ColoredLogger("Test").get_logger()
    logger.debug("Messaggio DEBUG")
    logger.info("Messaggio INFO")
    logger.warning("Messaggio WARNING")
    logger.error("Messaggio ERROR")
    logger.critical("Messaggio CRITICAL")
