from pathlib import Path
from utils.file_utils import create_dir, write_file, create_init
import shutil
import json

class ModuleGenerator:
    def __init__(self, module_name: str, base_path: str, is_main: bool = False, socket_enabled: bool = False):
        """
        Inizializza il generatore di moduli.
        :param module_name: Nome del modulo.
        :param base_path: Directory base in cui generare il modulo.
        :param is_main: Se True, il modulo verrà impostato come principale.
        :param socket_enabled: Se True, il modulo includerà il supporto socket.
        """
        self.module_name = module_name
        self.base_path = Path(base_path) / module_name
        self.is_main = is_main
        self.socket_enabled = socket_enabled
        # Percorso dello skeleton da copiare
        self.skeleton_path = Path(__file__).parent.parent.parent / "skeleton"

    def initialize(self, config: dict):
        pass

    def start(self):
        self.generate()

    def stop(self):
        pass

    def generate(self):
        # Crea la directory base
        create_dir(self.base_path)
        # Copia lo skeleton (struttura completa) nella directory del modulo
        try:
            shutil.copytree(self.skeleton_path, self.base_path, dirs_exist_ok=True)
            print(f"[INFO] Struttura copiata da '{self.skeleton_path}' a '{self.base_path}'")
        except Exception as e:
            print(f"[ERROR] Errore durante la copia dello skeleton: {e}")
            return
        
        # Personalizza il file di configurazione sostituendo il placeholder {MODULE_NAME}
        config_file = self.base_path / "config" / "default.py"
        if config_file.exists():
            content = config_file.read_text(encoding="utf-8")
            content = content.replace("{MODULE_NAME}", self.module_name)
            config_file.write_text(content, encoding="utf-8")
        
        # Aggiorna il manifest del modulo
        manifest_content = {
            "name": self.module_name,
            "is_main": self.is_main,
            "components": {
                "api": str((self.base_path / "api").resolve()),
                "ui": str((self.base_path / "ui").resolve()),
                "sockets": str((self.base_path / "sockets").resolve()),
                "controllers": str((self.base_path / "controllers").resolve()),
                "services": str((self.base_path / "services").resolve()),
                "models": str((self.base_path / "models").resolve()),
                "db": str((self.base_path / "db").resolve()),
                "utils": str((self.base_path / "utils").resolve()),
                "docs": str((self.base_path / "docs").resolve()),
                "config": str((self.base_path / "config").resolve()),
                "tests": str((self.base_path / "tests").resolve()),
                "interfaces": str((self.base_path / "interfaces").resolve()),
                "async": str((self.base_path / "async").resolve()),
                "auth": str((self.base_path / "auth").resolve()),
                "realtime": str((self.base_path / "realtime").resolve())
            }
        }
        manifest_file = self.base_path / "module_manifest.json"
        with manifest_file.open("w", encoding="utf-8") as f:
            json.dump(manifest_content, f, indent=4)
        
        print(f"[INFO] Modulo '{self.module_name}' generato correttamente in '{self.base_path.parent}'.")
