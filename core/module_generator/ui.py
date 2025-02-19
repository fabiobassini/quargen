# core/module_generator/ui.py
from pathlib import Path
from utils.file_utils import create_dir, write_file, read_file

def generate_ui_templates(base_path: Path, module_name: str, is_main: bool = False):
    m = module_name
    ui_dir = base_path / 'ui'
    templates_dir = ui_dir / 'templates'
    create_dir(templates_dir)
    
    # Template base: legge il file da "templates/html_templates/base/ui_base_template.html"
    base_template_path = Path("templates/html_templates/base/ui_base_template.html")
    base_html = read_file(base_template_path).replace("{{ module_name }}", m)
    base_templates_dir = templates_dir / 'base'
    create_dir(base_templates_dir)
    write_file(base_templates_dir / 'base.html', base_html)
    
    # Template index: legge il file da "templates/html_templates/ui_index_template.html"
    index_template_path = Path("templates/html_templates/ui_index_template.html")
    index_html = read_file(index_template_path).replace("{{ module_name }}", m)
    index_templates_dir = templates_dir / 'index'
    create_dir(index_templates_dir)
    write_file(index_templates_dir / 'index.html', index_html)
    
    # Creazione della cartella per gli endpoints extra (se necessari)
    endpoints_dir = ui_dir / 'endpoints'
    create_dir(endpoints_dir)
