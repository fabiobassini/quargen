from pathlib import Path
from utils.file_utils import create_dir, write_file

class ClassAdder:
    def add(self, type_: str, class_name: str, module_dir: str, url_prefix: str = None, subtype: str = None, prefix: str = None):
        module_path = Path(module_dir)
        target_dir = None
        filename = None
        filled = None

        if type_ == "controller":
            if not subtype:
                subtype = "rest"  # Default per controller
            if subtype == "rest":
                target_dir = module_path / "controllers" / "rest"
                custom_route = url_prefix if url_prefix is not None else "/"
                template = '''"""
Questo file definisce un controller REST per il modulo {module_name}.
Scopo: Gestire richieste API REST e restituire risposte in formato JSON.
Esempio:
    Una richiesta GET a "{{{{CONFIG["controller_blueprint_prefix"]}}}}{custom_route}" attiverà il metodo custom_action.
"""

from interfaces.business import IController
from flask import Blueprint, request, jsonify
from utils.logger import ColoredLogger
from ...config.default import CONFIG

logger = ColoredLogger(__name__).get_logger()

class {class_name}(IController):
    def __init__(self):
        # Il blueprint usa un nome univoco basato sul modulo e sul nome della classe
        self.blueprint = Blueprint('{module_name}_{class_name_lower}_controller', __name__, url_prefix=CONFIG["controller_blueprint_prefix"])
        self.register_routes()

    def register_routes(self):
        @self.blueprint.route('{custom_route}', methods=['GET'])
        def custom_action():
            logger.info("Richiesta custom route da {class_name}")
            return jsonify({{"message": "Risposta da {class_name}"}})
    
    def get_blueprint(self):
        return self.blueprint

    def action(self):
        return "Azione eseguita da {class_name}"
'''
                filled = template.format(module_name=module_path.name,
                                        class_name=class_name,
                                        class_name_lower=class_name.lower(),
                                        custom_route=custom_route)
                filename = target_dir / (class_name.lower() + ".py")




            elif subtype == "web":
                target_dir = module_path / "controllers" / "web"
                template = '''"""
Questo file definisce un controller web per il modulo {module_name}.
Scopo: Renderizzare template HTML per la UI.
Esempio:
    Il metodo action renderizzerà il template {template_file}.
"""

from interfaces.business import IController
from flask import render_template
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class {class_name}(IController):
    def action(self):
        return render_template('{template_file}')
'''
                filled = template.format(module_name=module_path.name, class_name=class_name, template_file=class_name.lower()+".html")
                filename = target_dir / (class_name.lower() + ".py")
        # ... (gli altri tipi restano invariati)
        elif type_ == "service":
            if not subtype:
                subtype = "business"
            if subtype == "business":
                target_dir = module_path / "services" / "business"
                template = '''"""
Questo file definisce un service di business per il modulo {module_name}.
Scopo: Implementare la logica di business dell'applicazione.
Esempio:
    Il metodo serve esegue la logica e restituisce un risultato.
"""

from interfaces.business import IService
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class {class_name}(IService):
    def serve(self):
        logger.info("Esecuzione di {class_name}")
        return "Risultato da {class_name}"
'''
                filled = template.format(module_name=module_path.name, class_name=class_name)
                filename = target_dir / (class_name.lower() + ".py")
            elif subtype == "data":
                target_dir = module_path / "services" / "data"
                template = '''"""
Questo file definisce un service per l'accesso ai dati per il modulo {module_name}.
Scopo: Recuperare i dati necessari dall'origine dati.
Esempio:
    Il metodo get_data restituisce i dati richiesti.
"""

from interfaces.data import IDataAccess

class {class_name}(IDataAccess):
    def get_data(self):
        return "Dati ottenuti da {class_name}"
'''
                filled = template.format(module_name=module_path.name, class_name=class_name)
                filename = target_dir / (class_name.lower() + ".py")
            else:
                print(f"[ERROR] Sottotipo di service '{subtype}' non supportato. Usa: business, data.")
                return
        elif type_ == "model":
            if not subtype:
                subtype = "domain"
            if subtype == "domain":
                target_dir = module_path / "models" / "domain"
                template = '''"""
Questo file definisce un modello di dominio per il modulo {module_name}.
Scopo: Rappresentare le entità e la logica di business sui dati.
Esempio:
    Il modello SampleModel gestisce i dati e li elabora.
"""

from interfaces.business import IModel

class {class_name}(IModel):
    def __init__(self, data):
        self.data = data

    def process(self):
        return f"Elaborazione dati da {class_name}: {{self.data}}"
'''
                filled = template.format(module_name=module_path.name, class_name=class_name)
                filename = target_dir / (class_name.lower() + ".py")
            elif subtype == "dto":
                target_dir = module_path / "models" / "dto"
                template = '''"""
Questo file definisce un Data Transfer Object (DTO) per il modulo {module_name}.
Scopo: Facilitare il trasferimento di dati tra i componenti dell'applicazione.
Esempio:
    Un DTO che converte gli attributi in dizionario.
"""

class {class_name}:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def to_dict(self):
        return self.__dict__
'''
                filled = template.format(module_name=module_path.name, class_name=class_name)
                filename = target_dir / (class_name.lower() + ".py")
            else:
                print(f"[ERROR] Sottotipo di model '{subtype}' non supportato. Usa: domain, dto.")
                return
        elif type_ == "template":
            target_dir = module_path / "ui" / "templates" / class_name.lower()
            create_dir(target_dir)
            template = r'''{{#
Questo file HTML è un template per la UI del modulo.
Scopo: Fornire una base per il rendering di pagine web.
Esempio:
    Il template estende "base/base.html" e definisce un blocco "content".
#}}

{{% extends "base/base.html" %}}

{{% block content %}}
<h2>{class_name} Template</h2>
<p>Contenuto personalizzato per {class_name}.</p>
{{% endblock %}}
'''
            filled = template.format(class_name=class_name)
            filename = target_dir / (class_name.lower() + ".html")
            static_css = module_path / "ui" / "static" / "css" / (class_name.lower() + ".css")
            static_js = module_path / "ui" / "static" / "js" / (class_name.lower() + ".js")
            write_file(static_css, f"/* Stili per {class_name} */\n")
            write_file(static_js, f"// Script per {class_name}\n")
            if url_prefix:
                endpoints_dir = module_path / "ui" / "endpoints"
                create_dir(endpoints_dir)
                endpoint_filename = endpoints_dir / (class_name.lower() + "_endpoint.py")
                view_name = class_name.lower() + "_view"
                endpoint_template = r'''"""
Questo file definisce un endpoint extra per il template {class_name}.
Scopo: Aggiungere funzionalità extra alla UI.
Esempio:
    L'endpoint viene registrato con il prefisso '{url_prefix}'.
"""

from flask import render_template
from utils.logger import ColoredLogger
logger = ColoredLogger(__name__).get_logger()

def register_endpoint(parent_bp):
    @parent_bp.route('{url_prefix}')
    def {view_name}():
        logger.info("Richiesta per {class_name} endpoint")
        return render_template('{template_folder}/{template_file}')
'''
                endpoint_content = endpoint_template.format(
                    url_prefix=url_prefix,
                    view_name=view_name,
                    class_name=class_name,
                    template_folder=class_name.lower(),
                    template_file=class_name.lower() + ".html"
                )
                write_file(endpoint_filename, endpoint_content)
        elif type_ == "endpoint":
            if not prefix:
                print("[ERROR] Per il tipo 'endpoint' è necessario specificare --prefix.")
                return
            target_dir = module_path / "api" / "endpoints"
            create_dir(target_dir)
            # La parte custom (in questo caso la route specifica) viene presa dal parametro prefix
            custom_route = prefix
            template = '''
"""
Questo file definisce un endpoint API aggiuntivo per il modulo {module_name}.
Scopo: Fornire funzionalità extra alle API del modulo.
Esempio:
    L'endpoint sarà accessibile su "{{{{CONFIG["api_blueprint_prefix"]}}}}{custom_route}".
"""
from flask import Blueprint, jsonify
from utils.logger import ColoredLogger
from ...config.default import CONFIG

logger = ColoredLogger(__name__).get_logger()

# Il blueprint usa un nome univoco basato sul modulo e sul nome della classe
api_endpoint_bp = Blueprint('{module_name}_{class_name_lower}_endpoint', __name__, url_prefix=CONFIG["api_blueprint_prefix"])

@api_endpoint_bp.route('{custom_route}', methods=['GET'])
def endpoint_home():
    logger.info("Richiesta per l'endpoint {custom_route}")
    return jsonify({{"message": "Risposta dall'endpoint {custom_route}"}})

def get_endpoint():
    return api_endpoint_bp
'''
            filled = template.format(module_name=module_path.name,
                                    class_name_lower=class_name.lower(),
                                    custom_route=custom_route)
            filename = target_dir / (class_name.lower() + "_endpoint.py")



        elif type_ == "db":
            target_dir = module_path / "db"
            template = '''
"""
Questo file definisce una classe custom per il database del modulo {module_name}.
Utilizzo:
    - Estende la logica di base per operazioni specifiche sul database.
            
Assicurati che questa classe implementi l’interfaccia IDatabase per mantenere coerenza.
"""

from interfaces.db import IDatabase

class {class_name}(IDatabase):
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.connection = None

    def connect(self):
        self.connection = f"Connected to {{self.db_url}}"
        print(f"[DB] {{self.connection}}")

    def disconnect(self):
        print("[DB] Disconnected")
        self.connection = None

    def execute(self, query: str, params: dict = None):
        print(f"[DB] Executing query: {{query}} with params: {{params}}")
        return []
'''
            filled = template.format(module_name=module_path.name, class_name=class_name)
            filename = target_dir / (class_name.lower() + ".py")
        else:
            print(f"[ERROR] Tipo '{type_}' non supportato. Usa: controller, service, model, template, endpoint.")
            return

        if target_dir is None or filename is None or filled is None:
            print("[ERROR] Impossibile generare il file per il tipo:", type_)
            return

        create_dir(target_dir)
        write_file(filename, filled)
        print(f"[ADD] Classe/template '{class_name}' aggiunta in {target_dir}")
