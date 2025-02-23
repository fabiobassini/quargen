"""
Interfacce per la logica di business.
"""

from abc import ABC, abstractmethod

class IModel(ABC):
    @abstractmethod
    def process(self):
        pass

class IController(ABC):
    @abstractmethod
    def action(self):
        pass

class IService(ABC):
    @abstractmethod
    def serve(self):
        pass
