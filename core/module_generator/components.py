# core/module_generator/components.py
from pathlib import Path
from utils.file_utils import write_file
from templates import api_template, ui_template, socket_template, model_template, controller_template, service_template

def generate_components(base_path: Path, module_name: str, socket_enabled: bool = False):
    m = module_name
    # Genera il modulo API: serve per esporre endpoint REST pubblici.
    write_file(base_path / "api" / "api_module.py", api_template.API_TEMPLATE.format(module_name=m))
    
    # Genera il modulo UI: gestisce il rendering dei template per l'interfaccia utente.
    write_file(base_path / "ui" / "ui_module.py", ui_template.UI_TEMPLATE.format(module_name=m))
    
    # Se il supporto socket è abilitato, genera il modulo socket.
    if socket_enabled:
        write_file(base_path / "sockets" / "socket_module.py", socket_template.SOCKET_TEMPLATE.format(module_name=m))
    else:
        placeholder = '''
"""
Socket module non abilitato.
Questo modulo non include funzionalità socket.
Utilizzo:
    Se CONFIG["socket_enabled"] è False, questa funzione initialize_socket restituisce None.
"""

def initialize_socket(config: dict):
    return None
    '''
    write_file(base_path / "sockets" / "socket_module.py", placeholder)


    
    # Genera un sample model che rappresenta il dominio dei dati.
    write_file(base_path / "models" / "domain" / "sample_model.py", model_template.DOMAIN_MODEL_TEMPLATE.format(module_name=m))
    
    # Genera un sample controller REST per gestire richieste API.
    write_file(base_path / "controllers" / "rest" / "sample_controller.py", controller_template.REST_CONTROLLER_TEMPLATE.format(module_name=m))
    
    # Genera un sample service per la logica di business.
    write_file(base_path / "services" / "business" / "sample_service.py", service_template.BUSINESS_SERVICE_TEMPLATE.format(module_name=m))
