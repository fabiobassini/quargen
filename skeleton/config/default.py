# Configurazione di default per il modulo {MODULE_NAME}
CONFIG = {
    "api_port": 5000,
    "ui_theme": "light",
    "socket_enabled": False,
    "module_name": "{MODULE_NAME}",
    # Prefissi di base per i blueprint:
    "api_blueprint_prefix": "/api",              # Per ogni API, di default: /api
    "controller_blueprint_prefix": "/controller",# Per ogni controller, di default: /controller
    # Route custom di default per il sample (parte dinamica, da usare nel decorator)
    "sample_controller_route": "/sample",        # Per il sample controller: /sample
    "ui_url_prefix": "/"                         # Per la UI: /
}
