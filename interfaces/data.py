# interfaces/data.py
from abc import ABC, abstractmethod

class IDataAccess(ABC):
    @abstractmethod
    def get_data(self):
        """Recupera i dati necessari."""
        pass

class IBusinessLogic(ABC):
    @abstractmethod
    def execute(self):
        """Esegue la logica di business."""
        pass
