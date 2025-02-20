import os
import sys
import json
import argparse
import importlib
from pathlib import Path
from flask import Flask

def load_module_manifest(module_dir: Path) -> dict:
    manifest_file = module_dir / "module_manifest.json"
    if manifest_file.exists():
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("[ERROR] Impossibile leggere il manifest in " + str(module_dir) + ": " + str(e))
    else:
        print("[WARN] Nessun file module_manifest.json trovato in " + str(module_dir))
    return {}

def find_modules_in_repo(repo_path: Path) -> list:
    """
    Scansiona ricorsivamente il repository (repo_path) e restituisce una lista di tuple
    (module_name, module_path) per ogni modulo individuato (ossia ogni cartella contenente un file "module_manifest.json").
    """
    modules = []
    for manifest in repo_path.rglob("module_manifest.json"):
        module_dir = manifest.parent.resolve()
        modules.append((module_dir.name, module_dir))
    return modules

def generate_aggregated_main(modules_info: list, output_dir: Path):
    """
    Crea il file main.py nell'output che:
      - Aggiunge in sys.path i percorsi dei genitori dei moduli (per renderli importabili come package)
      - Importa dinamicamente il main di ciascun modulo e registra i blueprint
      - Avvia l'app Flask aggregata
    """
    main_template = '''"""
Questo file viene generato automaticamente per aggregare i moduli forniti.
"""

import sys
import os
from flask import Flask
import importlib

app = Flask(__name__)

# Aggiungo i percorsi dei genitori dei moduli alla sys.path
MODULES = [
{modules_list}
]

for mod in MODULES:
    module_name = mod["name"]
    module_path = mod["path"]
    # Aggiungo il genitore del modulo a sys.path
    parent_dir = os.path.abspath(os.path.join(module_path, os.pardir))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    try:
        # Importa il modulo come package: MyApp.main
        module_main = importlib.import_module(module_name + ".main")
        if hasattr(module_main, "register_blueprints"):
            print("[INFO] Registrazione blueprint per il modulo " + module_name)
            module_main.register_blueprints(app)
        else:
            # Prova a cercare eventuali classi con il metodo get_blueprint
            for attr in dir(module_main):
                obj = getattr(module_main, attr)
                if callable(obj) and hasattr(obj, "get_blueprint"):
                    instance = obj()
                    bp = instance.get_blueprint()
                    if bp:
                        app.register_blueprint(bp)
                        print("[INFO] Registrato blueprint da " + module_name + " -> " + attr)
    except Exception as e:
        print("[ERROR] Problema nell'importare il modulo " + module_name + ": " + str(e))

if __name__ == "__main__":
    print("[MAIN] Avvio dell'app aggregata...")
    app.run(debug=True, port=5000)
'''

    # Prepara la lista dei moduli da inserire nel template
    modules_list_str = ""
    for mod in modules_info:
        modules_list_str += '    {"name": "' + mod[0] + '", "path": "' + str(mod[1]) + '"},\n'

    main_content = main_template.format(modules_list=modules_list_str.rstrip())

    output_file = output_dir / "main.py"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(main_content)
    print("[INFO] Aggregated main.py generato in " + str(output_file))

def main():
    parser = argparse.ArgumentParser(
        description="Aggregatore di moduli: scansiona repository di moduli QuarGen distinti e genera un'app aggregata."
    )
    parser.add_argument("--modules", nargs="+", required=True,
                        help="Percorsi alle repository dei moduli (ogni repo può contenere uno o più moduli)")
    parser.add_argument("--output", required=True,
                        help="Cartella di output dove generare il progetto aggregato")
    args = parser.parse_args()

    aggregated_modules = []
    for repo in args.modules:
        repo_path = Path(repo)
        if not repo_path.exists():
            print("[ERROR] La repository " + repo + " non esiste.")
            continue
        modules = find_modules_in_repo(repo_path)
        if modules:
            print("[INFO] Trovati " + str(len(modules)) + " modulo/i in " + repo)
            aggregated_modules.extend(modules)
        else:
            print("[WARN] Nessun modulo trovato in " + repo)

    if not aggregated_modules:
        print("[ERROR] Nessun modulo valido trovato. Interrompo l'aggregazione.")
        sys.exit(1)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    print("[INFO] Cartella di output: " + str(output_dir.resolve()))

    generate_aggregated_main(aggregated_modules, output_dir)
    print("[INFO] Operazione completata. Puoi avviare l'app aggregata eseguendo il main.py nell'output.")

if __name__ == "__main__":
    main()
