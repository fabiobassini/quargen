# core/module_generator/config_files.py

from pathlib import Path
import json
from utils.file_utils import write_file
from templates import config_template

def generate_config_files(base_path: Path, module_name: str):
    m = module_name
    env_content = f"# Variabili d'ambiente per il modulo {m}\nFLASK_ENV=development\nDEBUG=True\n"
    write_file(base_path / '.env', env_content)
    readme_content = f"# {m}\nModulo generato automaticamente per QuarTrend.\n"
    write_file(base_path / 'README.md', readme_content)
    write_file(base_path / 'requirements.txt', "Flask==2.1.2\n")
    write_file(base_path / "config" / "default.py", config_template.CONFIG_TEMPLATE.format(module_name=m))
    install_content = (
        f"# Installazione di {m}\n\n"
        "1. Clona il repository.\n"
        "2. Installa le dipendenze con: pip install -r requirements.txt\n"
        "3. Configura il file config/default.py.\n"
    )
    usage_content = (
        f"# Uso di {m}\n\n"
        f"- API: /api/{m}/...\n"
        "- UI: / (pagina index)\n"
        "- Sockets: se abilitati\n"
    )
    write_file(base_path / "docs" / "installation.md", install_content)
    write_file(base_path / "docs" / "usage.md", usage_content)

def generate_manifest(base_path: Path, module_name: str, is_main: bool):
    manifest = {
        "name": module_name,
        "is_main": is_main,
        "components": {
            "api": str((base_path / "api").resolve()),
            "ui": str((base_path / "ui").resolve()),
            "sockets": str((base_path / "sockets").resolve()),
            "controllers": str((base_path / "controllers").resolve()),
            "services": str((base_path / "services").resolve()),
            "models": str((base_path / "models").resolve())
        }
    }
    manifest_path = base_path / "module_manifest.json"
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)