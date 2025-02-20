# templates/py_templates/main_template.py
"""
Questo file è il punto di ingresso dell'applicazione generata da QuarGen.
Serve a inizializzare i moduli API, UI e, se abilitato, i socket, e a registrare automaticamente i controllers e gli endpoint.
Utilizzo:
    - Avviare l'applicazione eseguendo questo file.
    - Se CONFIG["socket_enabled"] è True, viene utilizzato Flask-SocketIO per la comunicazione in tempo reale.
"""

from flask import Flask
from .config.default import CONFIG
from .api.api_module import initialize_api
from .ui.ui_module import initialize_ui
from .sockets.socket_module import initialize_socket
import os
import importlib
from pathlib import Path

def register_controllers(app):
    pkg = Path(__file__).parent.name  # Ad esempio "MyApp"
    controllers_dir = os.path.join(os.path.dirname(__file__), 'controllers')
    with app.test_request_context():
        for root, dirs, files in os.walk(controllers_dir):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    module_path = os.path.join(root, file)
                    rel_path = os.path.relpath(module_path, os.path.dirname(__file__))[:-3].replace(os.sep, '.')
                    module_name = rel_path if rel_path.startswith(pkg) else pkg + '.' + rel_path
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
                        print(f"Errore nell'importare il modulo {module_name}: {e}")

def register_api_endpoints(app):
    """
    Registra automaticamente gli endpoint API presenti nella cartella 'api/'.
    Se il modulo ha una funzione get_endpoint() o get_blueprint(), il blueprint verrà registrato.
    """
    pkg = Path(__file__).parent.name  # Ad esempio "MyApp"
    # Scansiona SOLO la cartella 'api' (ricorsivamente, inclusi eventuali sottodirectory)
    base_dir = os.path.join(os.path.dirname(__file__), 'api')
    with app.test_request_context():
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    module_path = os.path.join(root, file)
                    rel_path = os.path.relpath(module_path, os.path.dirname(__file__))[:-3].replace(os.sep, '.')
                    module_name = rel_path if rel_path.startswith(pkg) else pkg + '.' + rel_path
                    try:
                        mod = importlib.import_module(module_name)
                        bp = None
                        if hasattr(mod, 'get_endpoint'):
                            bp = mod.get_endpoint()
                        elif hasattr(mod, 'get_blueprint'):
                            bp = mod.get_blueprint()
                        if bp:
                            app.register_blueprint(bp)
                    except Exception as e:
                        print(f"Errore nell'importare il modulo {module_name}: {e}")


def create_app():
    app = Flask(__name__, static_folder=None)
    api_mod = initialize_api(CONFIG)
    ui_mod = initialize_ui(CONFIG)
    socket_mod = initialize_socket(CONFIG)
    
    # Registra i blueprint principali
    app.register_blueprint(api_mod.get_api_blueprint())
    app.register_blueprint(ui_mod.get_ui_blueprint())
    
    # Registra automaticamente controllers e API endpoints
    register_controllers(app)
    register_api_endpoints(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    if CONFIG.get("socket_enabled"):
        from flask_socketio import SocketIO
        socketio = SocketIO(app)
        print("[MAIN] Avvio dell'applicazione con Flask-SocketIO...")
        socketio.run(app, debug=True, port=CONFIG["api_port"])
    else:
        print("[MAIN] Avvio dell'applicazione senza SocketIO...")
        app.run(debug=True, port=CONFIG["api_port"])
