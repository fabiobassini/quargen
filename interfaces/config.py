# interfaces/config.py
from abc import ABC, abstractmethod

class IConfigurable(ABC):
    @abstractmethod
    def load_config(self):
        """Carica la configurazione necessaria."""
        pass
