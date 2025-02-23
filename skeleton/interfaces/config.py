"""
Interfaccia per la configurazione.
"""

from abc import ABC, abstractmethod

class IConfigurable(ABC):
    @abstractmethod
    def load_config(self):
        pass
