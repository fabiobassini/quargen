# interfaces/business.py
from abc import ABC, abstractmethod

class IModel(ABC):
    @abstractmethod
    def process(self):
        """Elabora i dati e restituisce il risultato."""
        pass

class IController(ABC):
    @abstractmethod
    def action(self):
        """Esegue l'azione del controller."""
        pass

class IService(ABC):
    @abstractmethod
    def serve(self):
        """Esegue il servizio."""
        pass
