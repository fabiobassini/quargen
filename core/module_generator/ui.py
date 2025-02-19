# core/module_generator/ui.py
from pathlib import Path
from utils.file_utils import create_dir, write_file

def generate_ui_templates(base_path: Path, module_name: str, is_main: bool = False):
    m = module_name
    ui_dir = base_path / 'ui'
    templates_dir = ui_dir / 'templates'
    create_dir(templates_dir)
    # Template base
    base_templates_dir = templates_dir / 'base'
    create_dir(base_templates_dir)
    base_html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>{m} - Template Base</title>
    <link rel="stylesheet" href="{{{{ url_for('{m}_ui.static', filename='css/style.css') }}}}">
</head>
<body>
    <header>
        <h1>{m}</h1>
    </header>
    <main>
        {{% block content %}}
        <!-- Contenuto specifico del modulo -->
        {{% endblock %}}
    </main>
    <footer>
        <p>&copy; 2025 {m}. Tutti i diritti riservati.</p>
    </footer>
</body>
</html>"""
    write_file(base_templates_dir / 'base.html', base_html)
    # Template index
    index_templates_dir = templates_dir / 'index'
    create_dir(index_templates_dir)
    index_html = f"""{{% extends "base/base.html" %}}

{{% block content %}}
<h2>Benvenuto nel modulo {m}</h2>
<p>Questa è la pagina index di default.</p>
{{% endblock %}}
"""
    write_file(index_templates_dir / 'index.html', index_html)
    # Creazione della cartella per gli endpoints extra (se necessari)
    endpoints_dir = ui_dir / 'endpoints'
    create_dir(endpoints_dir)
    
    # Nota: la configurazione del blueprint (url_prefix e route) verrà gestita nel template Python
    # che si trova in templates/ui_template.py. Potresti voler aggiornare anche quel template per gestire
    # dinamicamente il url_prefix in base a is_main.
