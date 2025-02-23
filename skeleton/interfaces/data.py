"""
Interfaccia per l'accesso ai dati.
"""

from abc import ABC, abstractmethod

class IDataAccess(ABC):
    @abstractmethod
    def get_data(self):
        pass
