from pathlib import Path
from utils.file_utils import create_dir, write_file

def generate_static_assets(base_path: Path, module_name: str):
    m = module_name
    ui_dir = base_path / 'ui'
    static_dir = ui_dir / 'static'
    create_dir(static_dir)
    # CSS
    css_dir = static_dir / 'css'
    create_dir(css_dir)
    style_css = f"/* Stili di base per il modulo {m} */\nbody {{ font-family: Arial, sans-serif; background-color: #f5f5f5; }}"
    write_file(css_dir / 'style.css', style_css)
    # JavaScript
    js_dir = static_dir / 'js'
    create_dir(js_dir)
    script_js = f"// Script di base per il modulo {m}\ndocument.addEventListener('DOMContentLoaded', function() {{ console.log('Modulo {m} caricato'); }});"
    write_file(js_dir / 'script.js', script_js)
    # Immagini
    images_dir = static_dir / 'images'
    create_dir(images_dir)
