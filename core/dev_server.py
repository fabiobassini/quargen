import subprocess
import webbrowser
from pathlib import Path
from interfaces.core import IModule
import os

class DevServer(IModule):
    def __init__(self, module_path: str):
        self.module_path = Path(module_path)

    def initialize(self, config: dict):
        pass

    def start(self):
        print("[DEV] Avvio del server Flask in modalità sviluppo...")
        try:
            webbrowser.open("http://127.0.0.1:5000")
            # Imposta il working directory al genitore del modulo e avvia il modulo come package
            parent = self.module_path.parent
            module_name = self.module_path.name
            subprocess.run(["python", "-m", f"{module_name}.main"], cwd=parent, check=True)
        except Exception as e:
            print(f"[ERROR] Errore durante l'avvio del server: {e}")

    def stop(self):
        print("[DEV] Arresto del server Flask (operazione non implementata).")
