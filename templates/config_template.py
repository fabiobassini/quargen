# templates/config_template.py
CONFIG_TEMPLATE = """# Configurazione di default per il modulo {module_name}
# 
# Questo file definisce la configurazione base per il modulo.
# Scopo:
#    - Specificare le impostazioni fondamentali come porta API, tema UI e abilitazione dei socket.
# Utilizzo:
#    - Il file viene importato da main.py per inizializzare i vari moduli.
# Esempio:
#    CONFIG = {{
#         "api_port": 5000,
#         "ui_theme": "light",
#         "socket_enabled": True  # oppure False
#    }}
CONFIG = {{
    "api_port": 5000,
    "ui_theme": "light",
    "socket_enabled": {socket_enabled}
}}
"""


  

