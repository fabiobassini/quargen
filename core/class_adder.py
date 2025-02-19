# core/class_adder.py
from pathlib import Path
from utils.file_utils import create_dir, write_file

class ClassAdder:
    def add(self, type_: str, class_name: str, module_dir: str, url_prefix: str = None, subtype: str = None):
        module_path = Path(module_dir)
        if type_ == "controller":
            if not subtype:
                subtype = "rest"  # Default per controller
            if subtype == "rest":
                target_dir = module_path / "controllers" / "rest"
                template = '''from interfaces.business import IController
from flask import Blueprint, request, jsonify
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class {class_name}(IController):
    def __init__(self):
        self.blueprint = Blueprint('{module_name}_rest', __name__, url_prefix='/api/{module_name}')
        self.register_routes()

    def register_routes(self):
        @self.blueprint.route('/{route}', methods=['GET'])
        def sample():
            logger.info("Richiesta sample da {class_name}")
            return jsonify({{"message": "Risposta da {class_name}"}})
            
    def get_blueprint(self):
        return self.blueprint

    def action(self):
        return "Azione eseguita da {class_name}"
'''
                route = class_name.lower()
                filled = template.format(module_name=module_path.name, class_name=class_name, route=route)
            elif subtype == "web":
                target_dir = module_path / "controllers" / "web"
                template = '''from interfaces.business import IController
from flask import render_template
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class {class_name}(IController):
    def action(self):
        return render_template('{template_file}')
'''
                filled = template.format(module_name=module_path.name, class_name=class_name, template_file=class_name.lower()+".html")
            else:
                print(f"[ERROR] Sottotipo di controller '{subtype}' non supportato. Usa: rest, web.")
                return
            filename = target_dir / (class_name.lower() + ".py")
        elif type_ == "service":
            if not subtype:
                subtype = "business"
            if subtype == "business":
                target_dir = module_path / "services" / "business"
                template = '''from interfaces.business import IService
from utils.logger import ColoredLogger

logger = ColoredLogger(__name__).get_logger()

class {class_name}(IService):
    def serve(self):
        logger.info("Esecuzione di {class_name}")
        return "Risultato da {class_name}"
'''
                filled = template.format(module_name=module_path.name, class_name=class_name)
            elif subtype == "data":
                target_dir = module_path / "services" / "data"
                template = '''from interfaces.data import IDataAccess

class {class_name}(IDataAccess):
    def get_data(self):
        return "Dati ottenuti da {class_name}"
'''
                filled = template.format(module_name=module_path.name, class_name=class_name)
            else:
                print(f"[ERROR] Sottotipo di service '{subtype}' non supportato. Usa: business, data.")
                return
            filename = target_dir / (class_name.lower() + ".py")
        elif type_ == "model":
            if not subtype:
                subtype = "domain"
            if subtype == "domain":
                target_dir = module_path / "models" / "domain"
                template = '''from interfaces.business import IModel

class {class_name}(IModel):
    def __init__(self, data):
        self.data = data

    def process(self):
        return f"Elaborazione dati da {class_name}: {{self.data}}"
'''
                filled = template.format(module_name=module_path.name, class_name=class_name)
            elif subtype == "dto":
                target_dir = module_path / "models" / "dto"
                template = '''class {class_name}:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def to_dict(self):
        return self.__dict__
'''
                filled = template.format(module_name=module_path.name, class_name=class_name)
            else:
                print(f"[ERROR] Sottotipo di model '{subtype}' non supportato. Usa: domain, dto.")
                return
            filename = target_dir / (class_name.lower() + ".py")
        elif type_ == "template":
            target_dir = module_path / "ui" / "templates" / class_name.lower()
            create_dir(target_dir)
            # Utilizziamo un template con tag Jinja2 "escape-ati" (doppie parentesi) per preservare i tag
            template = r'''{{% extends "base/base.html" %}}

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
                endpoint_template = '''from flask import render_template
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
        else:
            print(f"[ERROR] Tipo '{type_}' non supportato. Usa: controller, service, model, template.")
            return
        create_dir(target_dir)
        write_file(filename, filled)
        print(f"[ADD] Classe/template '{class_name}' aggiunta in {target_dir}")
