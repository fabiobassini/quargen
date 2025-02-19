#!/usr/bin/env python3
import os
import argparse
from pathlib import Path

def create_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    print(f"Creata directory: {path}")

def write_file(path: Path, content: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Creato file: {path}")

# Template per .env
ENV_TEMPLATE = """# Variabili d'ambiente per il modulo {module_name}
FLASK_ENV=development
DEBUG=True
"""

# Template per README.md
README_TEMPLATE = """# {module_name}

Modulo generato automaticamente per QuarTrend.

## Descrizione

Questo modulo implementa le seguenti funzionalità:
- API (Flask blueprint)
- Interfaccia utente (UI) con template organizzati (base e estensioni)
- Gestione di socket (opzionale)
- Modelli, controller, servizi e utilità per la logica di business
- Test e documentazione

## Configurazione

Modifica i file in `config/` per personalizzare il comportamento del modulo.
"""

# Template per requirements.txt
REQUIREMENTS_TEMPLATE = """Flask==2.1.2
"""

# Template per config/default.py
CONFIG_TEMPLATE = """# Configurazione di default per il modulo {module_name}
CONFIG = {{
    "api_port": 5000,
    "ui_theme": "light",
    "socket_enabled": True
}}
"""

# Template per docs/installation.md
INSTALLATION_TEMPLATE = """# Installazione di {module_name}

Segui questi passi per installare e configurare il modulo:

1. Clona il repository.
2. Installa le dipendenze con: `pip install -r requirements.txt`
3. Configura il file `config/default.py` secondo le tue esigenze.
"""

# Template per docs/usage.md
USAGE_TEMPLATE = """# Uso di {module_name}

Descrizione di come utilizzare il modulo:

- **API**: Accedi agli endpoint API tramite `/api/{module_name}/...`
- **UI**: Visita la UI su `/{module_name}/`
- **Socket**: (Se abilitato) Gestione delle connessioni in tempo reale.

Consulta la documentazione per maggiori dettagli.
"""

# Template per __init__.py (root)
INIT_TEMPLATE = '''"""
Modulo {module_name} inizializzato per QuarTrend.
"""
from .api import api_module
from .ui import ui_module
from .socket import socket_module
'''

# Template per il modulo API (api/api_module.py)
API_TEMPLATE = '''from flask import Blueprint, jsonify

def get_api_blueprint():
    bp = Blueprint('{module_name}_api', __name__, url_prefix='/api/{module_name}')
    
    @bp.route('/status')
    def status():
        return jsonify({{"status": "API del modulo {module_name} attiva"}})
    
    return bp

def initialize_api(config: dict):
    print("Inizializzo l'API di {module_name} con config:", config)
'''

# Template per il modulo UI (ui/ui_module.py)
UI_TEMPLATE = '''from flask import Blueprint, render_template

def get_ui_blueprint():
    bp = Blueprint('{module_name}_ui', __name__, url_prefix='/{module_name}')
    
    @bp.route('/')
    def home():
        # Usa il template di base definito in ui/templates/base/base.html
        return render_template('base/base.html', module="{module_name}")
    
    return bp

def initialize_ui(config: dict):
    print("Inizializzo la UI di {module_name} con config:", config)
'''

# Template per il template HTML base (ui/templates/base/base.html)
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

# Template per il modulo Socket (socket/socket_module.py)
SOCKET_TEMPLATE = '''def handle_connection(connection):
    print("Gestisco la connessione nel modulo {module_name}: ", connection)

def initialize_socket(config: dict):
    print("Inizializzo il modulo socket di {module_name} con config:", config)
'''

# Template per models/__init__.py
MODELS_INIT_TEMPLATE = '''"""
Modelli per il modulo {module_name}
"""
'''

# Template per models/sample_model.py
SAMPLE_MODEL_TEMPLATE = '''class SampleModel:
    def __init__(self, data):
        self.data = data

    def process(self):
        return f"Elaborazione dati: {self.data}"
'''

# Template per controllers/__init__.py
CONTROLLERS_INIT_TEMPLATE = '''"""
Controller per il modulo {module_name}
"""
'''

# Template per controllers/sample_controller.py
SAMPLE_CONTROLLER_TEMPLATE = '''def sample_controller_action():
    return "Azione del controller di {module_name}"
'''

# Template per services/__init__.py
SERVICES_INIT_TEMPLATE = '''"""
Servizi per il modulo {module_name}
"""
'''

# Template per services/sample_service.py
SAMPLE_SERVICE_TEMPLATE = '''def sample_service():
    return "Servizio di {module_name} in esecuzione"
'''

# Template per utils/__init__.py
UTILS_INIT_TEMPLATE = '''"""
Utility per il modulo {module_name}
"""
'''

# Template per utils/logger.py
LOGGER_TEMPLATE = '''import logging

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
'''

# Template per tests/__init__.py
TESTS_INIT_TEMPLATE = '''"""
Test per il modulo {module_name}
"""
'''

# Template per tests/test_module.py (aggiornato per usare module_name_cap)
TEST_MODULE_TEMPLATE = '''import unittest
from {module_name} import api_module, ui_module

class Test{module_name_cap}(unittest.TestCase):
    def test_api_status(self):
        bp = api_module.get_api_blueprint()
        self.assertIsNotNone(bp)

    def test_ui_home(self):
        bp = ui_module.get_ui_blueprint()
        self.assertIsNotNone(bp)

if __name__ == '__main__':
    unittest.main()
'''

# Template per ui/static/css/style.css (con parentesi graffe escape)
STYLE_CSS_TEMPLATE = '''/* Stili di base per il modulo {module_name} */
body {{
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
}}
'''

# Template per ui/static/js/script.js (con parentesi graffe escape)
SCRIPT_JS_TEMPLATE = '''// Script JavaScript di base per il modulo {module_name}
document.addEventListener('DOMContentLoaded', function() {{
    console.log("Modulo {module_name} caricato");
}});
'''

def generate_module(module_name: str, base_path: str):
    # Percorso di base per il modulo
    module_path = Path(base_path) / module_name
    create_dir(module_path)
    
    # .env
    write_file(module_path / '.env', ENV_TEMPLATE.format(module_name=module_name))
    
    # README.md
    write_file(module_path / 'README.md', README_TEMPLATE.format(module_name=module_name))
    
    # requirements.txt
    write_file(module_path / 'requirements.txt', REQUIREMENTS_TEMPLATE)
    
    # Cartella config e file default.py
    config_dir = module_path / 'config'
    create_dir(config_dir)
    write_file(config_dir / 'default.py', CONFIG_TEMPLATE.format(module_name=module_name))
    
    # Cartella docs e file di documentazione
    docs_dir = module_path / 'docs'
    create_dir(docs_dir)
    write_file(docs_dir / 'installation.md', INSTALLATION_TEMPLATE.format(module_name=module_name))
    write_file(docs_dir / 'usage.md', USAGE_TEMPLATE.format(module_name=module_name))
    
    # Cartella models
    models_dir = module_path / 'models'
    create_dir(models_dir)
    write_file(models_dir / '__init__.py', MODELS_INIT_TEMPLATE.format(module_name=module_name))
    write_file(models_dir / 'sample_model.py', SAMPLE_MODEL_TEMPLATE)
    
    # Cartella controllers
    controllers_dir = module_path / 'controllers'
    create_dir(controllers_dir)
    write_file(controllers_dir / '__init__.py', CONTROLLERS_INIT_TEMPLATE.format(module_name=module_name))
    write_file(controllers_dir / 'sample_controller.py', SAMPLE_CONTROLLER_TEMPLATE.format(module_name=module_name))
    
    # Cartella services
    services_dir = module_path / 'services'
    create_dir(services_dir)
    write_file(services_dir / '__init__.py', SERVICES_INIT_TEMPLATE.format(module_name=module_name))
    write_file(services_dir / 'sample_service.py', SAMPLE_SERVICE_TEMPLATE.format(module_name=module_name))
    
    # Cartella utils
    utils_dir = module_path / 'utils'
    create_dir(utils_dir)
    write_file(utils_dir / '__init__.py', UTILS_INIT_TEMPLATE.format(module_name=module_name))
    write_file(utils_dir / 'logger.py', LOGGER_TEMPLATE)
    
    # Cartella tests
    tests_dir = module_path / 'tests'
    create_dir(tests_dir)
    write_file(tests_dir / '__init__.py', TESTS_INIT_TEMPLATE.format(module_name=module_name))
    write_file(tests_dir / 'test_module.py', TEST_MODULE_TEMPLATE.format(
        module_name=module_name,
        module_name_cap=module_name.capitalize()
    ))
    
    # __init__.py (root)
    write_file(module_path / '__init__.py', INIT_TEMPLATE.format(module_name=module_name))
    
    # Cartella API
    api_dir = module_path / 'api'
    create_dir(api_dir)
    write_file(api_dir / 'api_module.py', API_TEMPLATE.format(module_name=module_name))
    
    # Cartella UI e relativa struttura
    ui_dir = module_path / 'ui'
    create_dir(ui_dir)
    write_file(ui_dir / 'ui_module.py', UI_TEMPLATE.format(module_name=module_name))
    
    templates_dir = ui_dir / 'templates'
    create_dir(templates_dir)
    base_templates_dir = templates_dir / 'base'
    create_dir(base_templates_dir)
    write_file(base_templates_dir / 'base.html', BASE_HTML_TEMPLATE.format(module_name=module_name))
    
    # Cartella static all'interno della UI
    static_dir = ui_dir / 'static'
    create_dir(static_dir)
    # CSS
    css_dir = static_dir / 'css'
    create_dir(css_dir)
    write_file(css_dir / 'style.css', STYLE_CSS_TEMPLATE.format(module_name=module_name))
    # JavaScript
    js_dir = static_dir / 'js'
    create_dir(js_dir)
    write_file(js_dir / 'script.js', SCRIPT_JS_TEMPLATE.format(module_name=module_name))
    # Images (directory vuota)
    images_dir = static_dir / 'images'
    create_dir(images_dir)
    
    # Cartella Socket
    socket_dir = module_path / 'socket'
    create_dir(socket_dir)
    write_file(socket_dir / 'socket_module.py', SOCKET_TEMPLATE.format(module_name=module_name))

def main():
    parser = argparse.ArgumentParser(
        description="QuarTrend Module Generator: genera una struttura modulare completa e professionale."
    )
    parser.add_argument('--name', type=str, required=True,
                        help="Nome del modulo da creare")
    parser.add_argument('--base', type=str, default=".",
                        help="Directory di base in cui creare il modulo (default: directory corrente)")
    
    args = parser.parse_args()
    generate_module(args.name, args.base)
    print(f"\nModulo '{args.name}' generato correttamente in '{args.base}'.")

if __name__ == '__main__':
    main()
