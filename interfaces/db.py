from abc import ABC, abstractmethod

class IDatabase(ABC):
    @abstractmethod
    def connect(self):
        """Stabilisce una connessione al database."""
        pass

    @abstractmethod
    def disconnect(self):
        """Chiude la connessione al database."""
        pass

    @abstractmethod
    def execute(self, query: str, params: dict = None):
        """Esegue una query sul database."""
        pass
