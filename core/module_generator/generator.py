from pathlib import Path
from .directories import create_directories
from .config_files import generate_config_files
from .interfaces import generate_interfaces
from .components import generate_components
from .ui import generate_ui_templates
from .static_assets import generate_static_assets
from .main_files import generate_main_and_build_files

class ModuleGenerator:
    def __init__(self, module_name: str, base_path: str):
        self.module_name = module_name
        self.base_path = Path(base_path) / module_name

    def initialize(self, config: dict):
        pass

    def start(self):
        self.generate()

    def stop(self):
        pass

    def generate(self):
        create_directories(self.base_path)
        generate_config_files(self.base_path, self.module_name)
        generate_interfaces(self.base_path)
        generate_components(self.base_path, self.module_name)
        generate_ui_templates(self.base_path, self.module_name)
        generate_static_assets(self.base_path, self.module_name)
        generate_main_and_build_files(self.base_path, self.module_name)
        print(f"\n[INFO] Modulo '{self.module_name}' generato correttamente in '{self.base_path.parent}'.")
