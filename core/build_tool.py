# core/build_tool.py
import subprocess
from pathlib import Path

class BuildTool:
    def __init__(self, module_path: str):
        self.module_path = Path(module_path)

    def build(self):
        print("[BUILD] Avvio build in modalità produzione con webpack...")
        webpack_config = self.module_path / "webpack.config.js"
        if webpack_config.exists():
            try:
                subprocess.run(["npm", "install"], cwd=self.module_path, check=True)
                subprocess.run(["npx", "webpack"], cwd=self.module_path, check=True)
                print("[BUILD] Webpack build completato.")
            except Exception as e:
                print(f"[ERROR] Errore durante la build con webpack: {e}")
        else:
            print("[BUILD] webpack.config.js non trovato. Impossibile eseguire la build.")
