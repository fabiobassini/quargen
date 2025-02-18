from flask import Flask
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
