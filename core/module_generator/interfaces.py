# core/module_generator/interfaces.py

from pathlib import Path
from utils.file_utils import write_file

def generate_interfaces(base_path: Path):
    write_file(
        base_path / "interfaces" / "core.py",
r'''from abc import ABC, abstractmethod

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
''')
    write_file(
        base_path / "interfaces" / "data.py",
r'''from abc import ABC, abstractmethod

class IDataAccess(ABC):
    @abstractmethod
    def get_data(self):
        pass
''')
    write_file(
        base_path / "interfaces" / "config.py",
r'''from abc import ABC, abstractmethod

class IConfigurable(ABC):
    @abstractmethod
    def load_config(self):
        pass
''')
    write_file(
        base_path / "interfaces" / "business.py",
r'''from abc import ABC, abstractmethod

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
''')
