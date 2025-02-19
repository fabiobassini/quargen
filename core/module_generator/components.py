from pathlib import Path
from utils.file_utils import write_file
from templates import api_template, ui_template, socket_template, model_template, controller_template, service_template

def generate_components(base_path: Path, module_name: str):
    m = module_name
    write_file(base_path / "api" / "api_module.py", api_template.API_TEMPLATE.format(module_name=m))
    write_file(base_path / "ui" / "ui_module.py", ui_template.UI_TEMPLATE.format(module_name=m))
    write_file(base_path / "sockets" / "socket_module.py", socket_template.SOCKET_TEMPLATE.format(module_name=m))
    write_file(base_path / "models" / "domain" / "sample_model.py", model_template.DOMAIN_MODEL_TEMPLATE.format(module_name=m))
    write_file(base_path / "controllers" / "rest" / "sample_controller.py", controller_template.REST_CONTROLLER_TEMPLATE.format(module_name=m))
    write_file(base_path / "services" / "business" / "sample_service.py", service_template.BUSINESS_SERVICE_TEMPLATE.format(module_name=m))
