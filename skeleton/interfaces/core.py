"""
Interfaccia di base per i moduli.
"""

from abc import ABC, abstractmethod

class IModule(ABC):
    @abstractmethod
    def initialize(self, config: dict):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class IAPIModule(IModule):
    @abstractmethod
    def get_api_blueprint(self):
        pass

class IUIComponent(IModule):
    @abstractmethod
    def get_ui_blueprint(self):
        pass

class ISocketModule(IModule):
    @abstractmethod
    def handle_connection(self, connection):
        pass
