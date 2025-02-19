#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import webbrowser
import shutil
from pathlib import Path

# ===============================================
# Utility: creazione directory e scrittura file
# ===============================================
def create_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Creata directory: {path}")

def write_file(path: Path, content: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[INFO] Creato file: {path}")

# ===============================================
# Templates aggiornati
# ===============================================
ENV_TEMPLATE = """# Variabili d'ambiente per il modulo {module_name}
FLASK_ENV=development
DEBUG=True
"""

README_TEMPLATE = """# {module_name}

Modulo generato automaticamente per QuarTrend.

## Descrizione

Questo modulo implementa le seguenti funzionalità:
- API (Flask blueprint basato su classi)
- Interfaccia utente (UI) con template organizzati (cartelle base ed entry point index)
- Gestione di sockets (opzionale)
- Modelli, controller, servizi e utilità per la logica di business
- Test e documentazione

## Configurazione

Modifica i file in `config/` per personalizzare il comportamento del modulo.
"""

REQUIREMENTS_TEMPLATE = """Flask==2.1.2
"""

CONFIG_TEMPLATE = """# Configurazione di default per il modulo {module_name}
CONFIG = {{
    "api_port": 5000,
    "ui_theme": "light",
    "socket_enabled": True
}}
"""

INSTALLATION_TEMPLATE = """# Installazione di {module_name}

1. Clona il repository.
2. Installa le dipendenze con: `pip install -r requirements.txt`
3. Configura il file `config/default.py` secondo le tue esigenze.
"""

USAGE_TEMPLATE = """# Uso di {module_name}

- **API**: Accedi agli endpoint API tramite `/api/{module_name}/...`
- **UI**: Visita la UI su `/`
- **Sockets**: (Se abilitato) Gestione delle connessioni in tempo reale.

Consulta la documentazione per maggiori dettagli.
"""

INIT_TEMPLATE = '''"""
Modulo {module_name} inizializzato per QuarTrend.
"""
from .api import api_module
from .ui import ui_module
from .sockets import socket_module
'''

# API: basato su classe, con logger
API_TEMPLATE = '''from flask import Blueprint, jsonify
from utils.logger import ColoredLogger
logger = ColoredLogger(__name__).get_logger()

class APIModule:
    def __init__(self):
        self.blueprint = Blueprint('{module_name}_api', __name__, url_prefix='/api/{module_name}')
        self.register_routes()

    def register_routes(self):
        @self.blueprint.route('/status')
        def status():
            logger.info("Richiesta status API")
            return jsonify({{"status": "API del modulo {module_name} attiva"}})

    def get_blueprint(self):
        return self.blueprint

def initialize_api(config: dict):
    logger.info("Inizializzo l'API di {module_name} con config: " + str(config))
    return APIModule()
'''

# UI: blueprint creato con url_prefix='/' e con template_folder e static_folder impostati.
# In register_extra_endpoints, la stringa di log usa {{filename}} per non fare sostituzioni indesiderate.
UI_TEMPLATE = '''from flask import Blueprint, render_template
import os, importlib
from utils.logger import ColoredLogger
logger = ColoredLogger(__name__).get_logger()

class UIModule:
    def __init__(self):
        self.blueprint = Blueprint('{module_name}_ui', __name__, url_prefix='/', 
                                     template_folder='templates', static_folder='static', static_url_path='/static')
        self.register_routes()
        self.register_extra_endpoints()

    def register_routes(self):
        @self.blueprint.route('/')
        def home():
            logger.info("Richiesta pagina index")
            return render_template('index/index.html', module="{module_name}")

    def register_extra_endpoints(self):
        endpoints_dir = os.path.join(os.path.dirname(__file__), 'endpoints')
        if os.path.exists(endpoints_dir):
            for filename in os.listdir(endpoints_dir):
                if filename.endswith('_endpoint.py'):
                    mod_name = filename[:-3]
                    mod = importlib.import_module('ui.endpoints.' + mod_name)
                    if hasattr(mod, 'register_endpoint'):
                        mod.register_endpoint(self.blueprint)
                        logger.info("Registrato endpoint da {{filename}}")
                        
    def get_blueprint(self):
        return self.blueprint

def initialize_ui(config: dict):
    logger.info("Inizializzo la UI di {module_name} con config: " + str(config))
    return UIModule()
'''

# Sockets: rinominato in "sockets" per evitare conflitti
SOCKET_TEMPLATE = '''from utils.logger import ColoredLogger
logger = ColoredLogger(__name__).get_logger()

class SocketModule:
    def __init__(self):
        pass

    def handle_connection(self, connection):
        logger.info("Gestisco la connessione nel modulo {module_name}: " + str(connection))

def initialize_socket(config: dict):
    logger.info("Inizializzo il modulo sockets di {module_name} con config: " + str(config))
    return SocketModule()
'''

# Template per models, controllers, services
MODELS_INIT_TEMPLATE = '''"""
Modelli per il modulo {module_name}
"""
'''
SAMPLE_MODEL_TEMPLATE = '''class SampleModel:
    def __init__(self, data):
        self.data = data

    def process(self):
        return f"Elaborazione dati: {{self.data}}"
'''

CONTROLLERS_INIT_TEMPLATE = '''"""
Controller per il modulo {module_name}
"""
'''
SAMPLE_CONTROLLER_TEMPLATE = '''class SampleController:
    def action(self):
        return "Azione del controller di {module_name}"
'''

SERVICES_INIT_TEMPLATE = '''"""
Servizi per il modulo {module_name}
"""
'''
SAMPLE_SERVICE_TEMPLATE = '''class SampleService:
    def serve(self):
        return "Servizio di {module_name} in esecuzione"
'''

# Logger trasformato in classe con colori
LOGGER_TEMPLATE = '''import logging

class ColoredLogger:
    COLORS = {
        'DEBUG': '\\033[94m',     # Blu
        'INFO': '\\033[92m',      # Verde
        'WARNING': '\\033[93m',   # Giallo
        'ERROR': '\\033[91m',     # Rosso
        'CRITICAL': '\\033[95m'   # Magenta
    }
    RESET = '\\033[0m'

    class ColoredFormatter(logging.Formatter):
        def format(self, record):
            levelname = record.levelname
            if levelname in ColoredLogger.COLORS:
                record.levelname = "{}{}{}".format(ColoredLogger.COLORS[levelname], levelname, ColoredLogger.RESET)
            return super().format(record)

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setFormatter(self.ColoredFormatter('[%(levelname)s] %(message)s'))
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger
'''

UTILS_INIT_TEMPLATE = '''"""
Utility per il modulo (logger, etc.)
"""
'''

TESTS_INIT_TEMPLATE = '''"""
Test per il modulo {module_name}
"""
'''
TEST_MODULE_TEMPLATE = '''import unittest
from {module_name} import api_module, ui_module

class Test{module_name_cap}(unittest.TestCase):
    def test_api_status(self):
        mod = api_module.initialize_api({{}})
        self.assertIsNotNone(mod.get_blueprint())

    def test_ui_home(self):
        mod = ui_module.initialize_ui({{}})
        self.assertIsNotNone(mod.get_blueprint())

if __name__ == '__main__':
    unittest.main()
'''

# Template per il template HTML base
BASE_HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>{module_name} - Template Base</title>
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/style.css') }}}}">
</head>
<body>
    <header>
        <h1>{module_name}</h1>
    </header>
    <main>
        {{% block content %}}
        <!-- Contenuto specifico del modulo -->
        {{% endblock %}}
    </main>
    <footer>
        <p>&copy; 2025 {module_name}. Tutti i diritti riservati.</p>
    </footer>
</body>
</html>
'''

# Template per l'entry point index
INDEX_HTML_TEMPLATE = '''{{% extends "base/base.html" %}}

{{% block content %}}
<h2>Benvenuto nel modulo {module_name}</h2>
<p>Questa è la pagina index di default.</p>
{{% endblock %}}
'''

STYLE_CSS_TEMPLATE = '''/* Stili di base per il modulo {module_name} */
body {{
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
}}
'''
SCRIPT_JS_TEMPLATE = '''// Script JavaScript di base per il modulo {module_name}
document.addEventListener('DOMContentLoaded', function() {{
    console.log("Modulo {module_name} caricato");
}});
'''

# Template per il template UI (usato dal comando add template)
TEMPLATE_UI_TEMPLATE = '''{{% extends "base/base.html" %}}

{{% block content %}}
<h2>{class_name} Template</h2>
<p>Contenuto personalizzato per {class_name}.</p>
{{% endblock %}}
'''

# Template per l'endpoint generato (estensione di UIModule)
ENDPOINT_TEMPLATE = '''from flask import render_template
from utils.logger import ColoredLogger
logger = ColoredLogger(__name__).get_logger()

def register_endpoint(parent_bp):
    @parent_bp.route('{url_prefix}')
    def {view_name}():
        logger.info("Richiesta per {class_name} endpoint")
        return render_template('{template_folder}/{template_file}')
'''

# Template per main.py
MAIN_TEMPLATE = '''from flask import Flask
from config.default import CONFIG
from api.api_module import initialize_api
from ui.ui_module import initialize_ui
from sockets.socket_module import initialize_socket

def create_app():
    app = Flask(__name__)
    api_mod = initialize_api(CONFIG)
    ui_mod = initialize_ui(CONFIG)
    socket_mod = initialize_socket(CONFIG)
    app.register_blueprint(api_mod.get_blueprint())
    app.register_blueprint(ui_mod.get_blueprint())
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=CONFIG["api_port"])
'''

# Template per webpack.config.js (usa parentesi singole)
WEBPACK_CONFIG_TEMPLATE = '''const path = require('path');

module.exports = {
  mode: 'production',
  entry: './ui/static/js/script.js',
  output: {
    filename: 'script.min.js',
    path: path.resolve(__dirname, 'ui/static/js')
  }
};
'''

# Template per package.json
PACKAGE_JSON_TEMPLATE = '''{{
  "name": "{module_name}",
  "version": "1.0.0",
  "private": true,
  "devDependencies": {{
    "webpack": "^5.0.0",
    "webpack-cli": "^4.0.0"
  }}
}}
'''

# ===============================================
# Classe ModuleGenerator: genera la struttura completa
# ===============================================
class ModuleGenerator:
    def __init__(self, module_name: str, base_path: str):
        self.module_name = module_name
        self.base_path = Path(base_path) / module_name

    def generate(self):
        m = self.module_name
        create_dir(self.base_path)
        write_file(self.base_path / '.env', ENV_TEMPLATE.format(module_name=m))
        write_file(self.base_path / 'README.md', README_TEMPLATE.format(module_name=m))
        write_file(self.base_path / 'requirements.txt', REQUIREMENTS_TEMPLATE)

        # config
        config_dir = self.base_path / 'config'
        create_dir(config_dir)
        write_file(config_dir / 'default.py', CONFIG_TEMPLATE.format(module_name=m))

        # docs
        docs_dir = self.base_path / 'docs'
        create_dir(docs_dir)
        write_file(docs_dir / 'installation.md', INSTALLATION_TEMPLATE.format(module_name=m))
        write_file(docs_dir / 'usage.md', USAGE_TEMPLATE.format(module_name=m))

        # models
        models_dir = self.base_path / 'models'
        create_dir(models_dir)
        write_file(models_dir / '__init__.py', MODELS_INIT_TEMPLATE.format(module_name=m))
        write_file(models_dir / 'sample_model.py', SAMPLE_MODEL_TEMPLATE)

        # controllers
        controllers_dir = self.base_path / 'controllers'
        create_dir(controllers_dir)
        write_file(controllers_dir / '__init__.py', CONTROLLERS_INIT_TEMPLATE.format(module_name=m))
        write_file(controllers_dir / 'sample_controller.py', SAMPLE_CONTROLLER_TEMPLATE.format(module_name=m))

        # services
        services_dir = self.base_path / 'services'
        create_dir(services_dir)
        write_file(services_dir / '__init__.py', SERVICES_INIT_TEMPLATE.format(module_name=m))
        write_file(services_dir / 'sample_service.py', SAMPLE_SERVICE_TEMPLATE.format(module_name=m))

        # utils
        utils_dir = self.base_path / 'utils'
        create_dir(utils_dir)
        write_file(utils_dir / '__init__.py', UTILS_INIT_TEMPLATE.format(module_name=m))
        write_file(utils_dir / 'logger.py', LOGGER_TEMPLATE)

        # tests
        tests_dir = self.base_path / 'tests'
        create_dir(tests_dir)
        write_file(tests_dir / '__init__.py', TESTS_INIT_TEMPLATE.format(module_name=m))
        write_file(tests_dir / 'test_module.py', TEST_MODULE_TEMPLATE.format(
            module_name=m,
            module_name_cap=m.capitalize()
        ))

        # __init__.py (root)
        write_file(self.base_path / '__init__.py', INIT_TEMPLATE.format(module_name=m))

        # api
        api_dir = self.base_path / 'api'
        create_dir(api_dir)
        write_file(api_dir / 'api_module.py', API_TEMPLATE.format(module_name=m))

        # ui
        ui_dir = self.base_path / 'ui'
        create_dir(ui_dir)
        write_file(ui_dir / 'ui_module.py', UI_TEMPLATE.format(module_name=m))
        templates_dir = ui_dir / 'templates'
        create_dir(templates_dir)
        # cartella base e relativo file base.html
        base_templates_dir = templates_dir / 'base'
        create_dir(base_templates_dir)
        write_file(base_templates_dir / 'base.html', BASE_HTML_TEMPLATE.format(module_name=m))
        # cartella index ed entry point index.html
        index_templates_dir = templates_dir / 'index'
        create_dir(index_templates_dir)
        write_file(index_templates_dir / 'index.html', INDEX_HTML_TEMPLATE.format(module_name=m))
        # Creazione della cartella endpoints per gli endpoint extra
        endpoints_dir = ui_dir / 'endpoints'
        create_dir(endpoints_dir)
        static_dir = ui_dir / 'static'
        create_dir(static_dir)
        css_dir = static_dir / 'css'
        create_dir(css_dir)
        write_file(css_dir / 'style.css', STYLE_CSS_TEMPLATE.format(module_name=m))
        js_dir = static_dir / 'js'
        create_dir(js_dir)
        write_file(js_dir / 'script.js', SCRIPT_JS_TEMPLATE.format(module_name=m))
        images_dir = static_dir / 'images'
        create_dir(images_dir)

        # sockets (rinominato in sockets)
        sockets_dir = self.base_path / 'sockets'
        create_dir(sockets_dir)
        write_file(sockets_dir / 'socket_module.py', SOCKET_TEMPLATE.format(module_name=m))

        # main.py
        write_file(self.base_path / 'main.py', MAIN_TEMPLATE)

        # webpack.config.js
        write_file(self.base_path / 'webpack.config.js', WEBPACK_CONFIG_TEMPLATE)

        # package.json
        write_file(self.base_path / 'package.json', PACKAGE_JSON_TEMPLATE.format(module_name=m))

        print(f"\n[INFO] Modulo '{m}' generato correttamente in '{self.base_path.parent}'.")

# ===============================================
# Comando Dev: avvia il server in modalità sviluppo
# ===============================================
class DevServer:
    def __init__(self, module_path: str = "."):
        self.module_path = Path(module_path)

    def run(self):
        print("[DEV] Avvio del server Flask in modalità sviluppo...")
        try:
            webbrowser.open("http://127.0.0.1:5000")
            subprocess.run(["python", "main.py"], cwd=self.module_path, check=True)
        except Exception as e:
            print(f"[ERROR] Errore durante l'avvio del server: {e}")

# ===============================================
# Comando Build: genera versione production usando webpack
# ===============================================
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

# ===============================================
# Comando Add: aggiunge una nuova classe o template
# ===============================================
class ClassAdder:
    def add(self, type_: str, class_name: str, module_dir: str, url_prefix: str = None):
        module_path = Path(module_dir)
        if type_ == "controller":
            target_dir = module_path / "controllers"
            template = '''class {class_name}:
    def action(self):
        return "Azione di {class_name} in {module_name}"
'''
            filename = target_dir / (class_name.lower() + ".py")
            filled = template.format(module_name=module_path.name, class_name=class_name)
        elif type_ == "service":
            target_dir = module_path / "services"
            template = '''class {class_name}:
    def serve(self):
        return "Servizio di {class_name} in {module_name}"
'''
            filename = target_dir / (class_name.lower() + ".py")
            filled = template.format(module_name=module_path.name, class_name=class_name)
        elif type_ == "template":
            target_dir = module_path / "ui" / "templates" / class_name.lower()
            create_dir(target_dir)
            template_content = TEMPLATE_UI_TEMPLATE.replace("{class_name}", class_name)
            filename = target_dir / (class_name.lower() + ".html")
            static_css = module_path / "ui" / "static" / "css" / (class_name.lower() + ".css")
            static_js = module_path / "ui" / "static" / "js" / (class_name.lower() + ".js")
            write_file(static_css, f"/* Stili per {class_name} */\n")
            write_file(static_js, f"// Script per {class_name}\n")
            filled = template_content
            # Se url_prefix è specificato, genera un endpoint che estende UIModule
            if url_prefix:
                endpoints_dir = module_path / "ui" / "endpoints"
                create_dir(endpoints_dir)
                endpoint_filename = endpoints_dir / (class_name.lower() + "_endpoint.py")
                view_name = class_name.lower() + "_view"
                # Il template assume che il template si trovi in ui/templates/<nome_template>/<nome_template>.html
                endpoint_content = ENDPOINT_TEMPLATE.format(
                    url_prefix=url_prefix,
                    view_name=view_name,
                    class_name=class_name,
                    template_folder=class_name.lower(),
                    template_file=class_name.lower() + ".html"
                )
                write_file(endpoint_filename, endpoint_content)
        else:
            print(f"[ERROR] Tipo '{type_}' non supportato. Usa: controller, service, template.")
            return
        create_dir(target_dir)
        write_file(filename, filled)
        print(f"[ADD] Classe/template '{class_name}' aggiunta in {target_dir}")

# ===============================================
# Classe principale per gestire i comandi CLI
# ===============================================
class QuarTrendCLI:
    @staticmethod
    def generate_module(args):
        gen = ModuleGenerator(args.name, args.base)
        gen.generate()

    @staticmethod
    def run_dev(args):
        dev = DevServer(args.module)
        dev.run()

    @staticmethod
    def run_build(args):
        builder = BuildTool(args.module)
        builder.build()

    @staticmethod
    def add_class(args):
        adder = ClassAdder()
        adder.add(args.type, args.class_name, args.module, getattr(args, 'url_prefix', None))

# ===============================================
# Main: definizione dei sub-comandi con argparse
# ===============================================
def main():
    parser = argparse.ArgumentParser(
        description="QuarTrend CLI: Strumenti per generare moduli (con main.py, webpack.config.js e package.json), avviare l'app in modalità sviluppo, buildare la versione di produzione tramite webpack, e aggiungere nuove classi/template.\n\nEsempi:\n  python quargen.py generate --name MyModule --base /percorso/progetto\n  python quargen.py dev --module /percorso/progetto/MyModule\n  python quargen.py build --module /percorso/progetto/MyModule\n  python quargen.py add --type template --class_name CustomTemplate --module /percorso/progetto/MyModule --url_prefix /custom",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Comando generate
    gen_parser = subparsers.add_parser("generate", help="Genera la struttura di un nuovo modulo (include main.py, webpack.config.js e package.json).")
    gen_parser.add_argument("--name", type=str, required=True, help="Nome del modulo da creare")
    gen_parser.add_argument("--base", type=str, default=".", help="Directory base per il modulo")
    gen_parser.set_defaults(func=QuarTrendCLI.generate_module)

    # Comando dev
    dev_parser = subparsers.add_parser("dev", help="Avvia l'applicazione in modalità sviluppo (usa main.py).")
    dev_parser.add_argument("--module", type=str, default=".", help="Percorso del modulo (directory contenente main.py)")
    dev_parser.set_defaults(func=QuarTrendCLI.run_dev)

    # Comando build
    build_parser = subparsers.add_parser("build", help="Esegue la build in modalità produzione tramite webpack (JS minimizzato).")
    build_parser.add_argument("--module", type=str, required=True, help="Percorso del modulo da buildare")
    build_parser.set_defaults(func=QuarTrendCLI.run_build)

    # Comando add
    add_parser = subparsers.add_parser("add", help="Aggiunge una nuova classe o template al modulo.")
    add_parser.add_argument("--type", type=str, required=True, choices=["controller", "service", "template"],
                            help="Tipo di classe/template da aggiungere")
    add_parser.add_argument("--class_name", type=str, required=True, help="Nome della nuova classe/template")
    add_parser.add_argument("--module", type=str, required=True, help="Percorso della directory del modulo")
    add_parser.add_argument("--url_prefix", type=str, default=None, help="(Opzionale, solo per template) URL prefix per l'endpoint da generare")
    add_parser.set_defaults(func=QuarTrendCLI.add_class)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
