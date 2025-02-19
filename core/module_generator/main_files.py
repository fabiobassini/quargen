# core/module_generator/main_files.py

from pathlib import Path
from utils.file_utils import write_file

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

def generate_main_and_build_files(base_path: Path, module_name: str):
    m = module_name
    write_file(base_path / 'main.py', MAIN_TEMPLATE.format(module_name=m))
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
    write_file(base_path / 'webpack.config.js', webpack_config)
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
    write_file(base_path / 'package.json', package_json)
