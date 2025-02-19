# core/module_generator.py
import os
from pathlib import Path
from utils.file_utils import create_dir, write_file, create_init
from templates import (
    api_template,
    ui_template,
    socket_template,
    config_template,
    model_template,         # DOMAIN_MODEL_TEMPLATE
    controller_template,    # REST_CONTROLLER_TEMPLATE
    service_template,       # BUSINESS_SERVICE_TEMPLATE
    # Per gli altri file, usiamo contenuto predefinito:
    # (ad esempio, per env, README, requirements, installation e usage, li generiamo inline)
)
from interfaces.core import IModule

# MAIN_TEMPLATE aggiornato: usa import relativi e registra automaticamente i controller
MAIN_TEMPLATE = '''from flask import Flask
from .config.default import CONFIG
from .api.api_module import initialize_api
from .ui.ui_module import initialize_ui
from .sockets.socket_module import initialize_socket
import os
import importlib

def register_controllers(app):
    pkg = __name__.split('.')[0]  # Es: "MyApp"
    controllers_dir = os.path.join(os.path.dirname(__file__), 'controllers')
    for root, dirs, files in os.walk(controllers_dir):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                module_path = os.path.join(root, file)
                rel_path = os.path.relpath(module_path, os.path.dirname(__file__))[:-3].replace(os.sep, '.')
                if not rel_path.startswith(pkg):
                    module_name = pkg + '.' + rel_path
                else:
                    module_name = rel_path
                try:
                    mod = importlib.import_module(module_name)
                    if hasattr(mod, 'get_blueprint'):
                        bp = mod.get_blueprint()
                        if bp:
                            app.register_blueprint(bp)
                    else:
                        for attr in dir(mod):
                            obj = getattr(mod, attr)
                            if callable(obj) and hasattr(obj, 'get_blueprint'):
                                bp = obj().get_blueprint()
                                if bp:
                                    app.register_blueprint(bp)
                except Exception as e:
                    print(f"Errore nell'importare il modulo {{module_name}}: {{e}}")

def create_app():
    app = Flask(__name__, static_folder=None)
    api_mod = initialize_api(CONFIG)
    ui_mod = initialize_ui(CONFIG)
    socket_mod = initialize_socket(CONFIG)
    app.register_blueprint(api_mod.get_api_blueprint())
    app.register_blueprint(ui_mod.get_ui_blueprint())
    register_controllers(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=CONFIG["api_port"])
'''

class ModuleGenerator(IModule):
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
        m = self.module_name
        # Elenco delle directory principali da creare
        dirs = [
            self.base_path,
            self.base_path / "config",
            self.base_path / "docs",
            self.base_path / "models" / "domain",
            self.base_path / "models" / "dto",
            self.base_path / "controllers" / "rest",
            self.base_path / "controllers" / "web",
            self.base_path / "services" / "business",
            self.base_path / "services" / "data",
            self.base_path / "utils",
            self.base_path / "tests",
            self.base_path / "api",
            self.base_path / "ui",
            self.base_path / "sockets",
            self.base_path / "interfaces"
        ]
        for d in dirs:
            create_dir(d)
            create_init(d)

        # Generazione dei file di configurazione e documentazione
        env_content = f"# Variabili d'ambiente per il modulo {m}\nFLASK_ENV=development\nDEBUG=True\n"
        write_file(self.base_path / '.env', env_content)
        readme_content = f"# {m}\nModulo generato automaticamente per QuarTrend.\n"
        write_file(self.base_path / 'README.md', readme_content)
        write_file(self.base_path / 'requirements.txt', "Flask==2.1.2\n")
        write_file(self.base_path / "config" / "default.py", config_template.CONFIG_TEMPLATE.format(module_name=m))
        install_content = f"# Installazione di {m}\n\n1. Clona il repository.\n2. Installa le dipendenze con: pip install -r requirements.txt\n3. Configura il file config/default.py.\n"
        usage_content = f"# Uso di {m}\n\n- API: /api/{m}/...\n- UI: / (pagina index)\n- Sockets: se abilitati\n"
        write_file(self.base_path / "docs" / "installation.md", install_content)
        write_file(self.base_path / "docs" / "usage.md", usage_content)

        # Creazione dei file delle interfacce
        write_file(self.base_path / "interfaces" / "core.py", 
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
        write_file(self.base_path / "interfaces" / "data.py", 
r'''from abc import ABC, abstractmethod

class IDataAccess(ABC):
    @abstractmethod
    def get_data(self):
        pass
''')
        write_file(self.base_path / "interfaces" / "config.py", 
r'''from abc import ABC, abstractmethod

class IConfigurable(ABC):
    @abstractmethod
    def load_config(self):
        pass
''')
        write_file(self.base_path / "interfaces" / "business.py",
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

        # Generazione dei componenti principali
        write_file(self.base_path / "api" / "api_module.py", api_template.API_TEMPLATE.format(module_name=m))
        write_file(self.base_path / "ui" / "ui_module.py", ui_template.UI_TEMPLATE.format(module_name=m))
        write_file(self.base_path / "sockets" / "socket_module.py", socket_template.SOCKET_TEMPLATE.format(module_name=m))
        
        # Sample business components
        write_file(self.base_path / "models" / "domain" / "sample_model.py", model_template.DOMAIN_MODEL_TEMPLATE.format(module_name=m))
        write_file(self.base_path / "controllers" / "rest" / "sample_controller.py", controller_template.REST_CONTROLLER_TEMPLATE.format(module_name=m))
        write_file(self.base_path / "services" / "business" / "sample_service.py", service_template.BUSINESS_SERVICE_TEMPLATE.format(module_name=m))
        
        # UI: creazione di templates e static
        ui_dir = self.base_path / 'ui'
        # Templates (generati in ui/templates)
        templates_dir = ui_dir / 'templates'
        create_dir(templates_dir)
        # Cartella base ed entry point base.html (corretta sintassi Jinja2)
        base_templates_dir = templates_dir / 'base'
        create_dir(base_templates_dir)
        base_html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>{m} - Template Base</title>
    <link rel="stylesheet" href="{{{{ url_for('{m}_ui.static', filename='css/style.css') }}}}">
</head>
<body>
    <header>
        <h1>{m}</h1>
    </header>
    <main>
        {{% block content %}}
        <!-- Contenuto specifico del modulo -->
        {{% endblock %}}
    </main>
    <footer>
        <p>&copy; 2025 {m}. Tutti i diritti riservati.</p>
    </footer>
</body>
</html>"""
        write_file(base_templates_dir / 'base.html', base_html)
        # Cartella index ed entry point index.html
        index_templates_dir = templates_dir / 'index'
        create_dir(index_templates_dir)
        index_html = f"""{{% extends "base/base.html" %}}

{{% block content %}}
<h2>Benvenuto nel modulo {m}</h2>
<p>Questa è la pagina index di default.</p>
{{% endblock %}}
"""
        write_file(index_templates_dir / 'index.html', index_html)
        # NON generiamo endpoints dentro templates, ma in ui/endpoints
        endpoints_dir = ui_dir / 'endpoints'
        create_dir(endpoints_dir)
        # Static: creazione della directory static e dei suoi sottopacchetti
        static_dir = ui_dir / 'static'
        create_dir(static_dir)
        css_dir = static_dir / 'css'
        create_dir(css_dir)
        style_css = f"/* Stili di base per il modulo {m} */\nbody {{ font-family: Arial, sans-serif; background-color: #f5f5f5; }}"
        write_file(css_dir / 'style.css', style_css)
        js_dir = static_dir / 'js'
        create_dir(js_dir)
        script_js = f"// Script di base per il modulo {m}\ndocument.addEventListener('DOMContentLoaded', function() {{ console.log('Modulo {m} caricato'); }});"
        write_file(js_dir / 'script.js', script_js)
        images_dir = static_dir / 'images'
        create_dir(images_dir)

        # main.py (con registrazione automatica dei controller)
        write_file(self.base_path / 'main.py', MAIN_TEMPLATE.format(module_name=m))
        # webpack.config.js e package.json (contenuto predefinito)
        webpack_config = """const path = require('path');

module.exports = {
  mode: 'production',
  entry: './ui/static/js/script.js',
  output: {
    filename: 'script.min.js',
    path: path.resolve(__dirname, 'ui/static/js')
  }
};
"""
        write_file(self.base_path / 'webpack.config.js', webpack_config)
        package_json = f"""{{
  "name": "{m}",
  "version": "1.0.0",
  "private": true,
  "devDependencies": {{
    "webpack": "^5.0.0",
    "webpack-cli": "^4.0.0"
  }}
}}
"""
        write_file(self.base_path / 'package.json', package_json)

        print(f"\n[INFO] Modulo '{m}' generato correttamente in '{self.base_path.parent}'.")
