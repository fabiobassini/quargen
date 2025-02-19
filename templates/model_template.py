# templates/model_template.py
DOMAIN_MODEL_TEMPLATE = '''"""
Questo file definisce un modello di dominio per il modulo {module_name}.
Scopo: Rappresentare le entità e la logica di business inerente ai dati.
Utilizzo:
    - Il modello gestisce dati e li elabora tramite il metodo process.
Esempio:
    - SampleModel(data).process() elaborerà i dati passati.
"""

from interfaces.business import IModel

class SampleModel(IModel):
    def __init__(self, data):
        self.data = data

    def process(self):
        # Implementa la logica di business per l'elaborazione del modello
        return f"Elaborazione dati nel dominio: {{self.data}}"
'''
