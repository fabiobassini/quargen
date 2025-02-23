"""
Punto di ingresso dell'applicazione generata dal modulo.
"""

from flask import Flask
from .config.default import CONFIG
from .api.api_module import initialize_api
from .ui.ui_module import initialize_ui
from .sockets.socket_module import initialize_socket
from .utils.logger import ColoredLogger
import os
import importlib
from pathlib import Path

def register_controllers(app):
    pkg = Path(__file__).parent.name  # Ad esempio, il nome del modulo
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
    pkg = Path(__file__).parent.name
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
    
    app.register_blueprint(api_mod.get_api_blueprint())
    app.register_blueprint(ui_mod.get_ui_blueprint())
    register_controllers(app)
    register_api_endpoints(app)
    return app

if __name__ == '__main__':
    logger = ColoredLogger("Main").get_logger()
    app = create_app()
    if CONFIG.get("socket_enabled"):
        from flask_socketio import SocketIO
        socketio = SocketIO(app)
        logger.info("Avvio dell'applicazione con SocketIO...")
        socketio.run(app, debug=True, port=CONFIG["api_port"])
    else:
        logger.info("Avvio dell'applicazione senza SocketIO...")
        app.run(debug=True, port=CONFIG["api_port"])
