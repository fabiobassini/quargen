# core/module_generator/generator.py
from pathlib import Path
from .directories import create_directories
from .config_files import generate_config_files, generate_manifest
from .interfaces import generate_interfaces
from .components import generate_components
from .ui import generate_ui_templates
from .static_assets import generate_static_assets
from .main_files import generate_main_and_build_files
from .db_assets import generate_db_assets
from .generate_logger import generate_logger


class ModuleGenerator:
    def __init__(self, module_name: str, base_path: str, is_main: bool = False, socket_enabled: bool = False):
        """
        Inizializza il generatore di moduli.
        
        :param module_name: Nome del modulo.
        :param base_path: Directory base in cui generare il modulo.
        :param is_main: Se True, il modulo verrà impostato come principale (endpoint '/' per la UI).
        :param socket_enabled: Se True, il modulo includerà il supporto per i socket.
        """
        self.module_name = module_name
        self.base_path = Path(base_path) / module_name
        self.is_main = is_main
        self.socket_enabled = socket_enabled

    def initialize(self, config: dict):
        pass

    def start(self):
        self.generate()

    def stop(self):
        pass

    def generate(self):
        create_directories(self.base_path)
        # Passa socket_enabled anche alla generazione dei file di config
        generate_config_files(self.base_path, self.module_name, socket_enabled=self.socket_enabled)
        generate_interfaces(self.base_path)
        generate_components(self.base_path, self.module_name, socket_enabled=self.socket_enabled)
        generate_ui_templates(self.base_path, self.module_name, self.is_main)
        generate_static_assets(self.base_path, self.module_name)
        generate_main_and_build_files(self.base_path, self.module_name)
        generate_manifest(self.base_path, self.module_name, self.is_main)
        generate_db_assets(self.base_path, self.module_name)
        generate_logger(self.base_path)
        print(f"\n[INFO] Modulo '{self.module_name}' generato correttamente in '{self.base_path.parent}'.")
