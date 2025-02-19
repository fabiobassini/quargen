# templates/model_template.py
DOMAIN_MODEL_TEMPLATE = '''from interfaces.business import IModel

class SampleModel(IModel):
    def __init__(self, data):
        self.data = data

    def process(self):
        # Implementa la logica di business per l'elaborazione del modello
        return f"Elaborazione dati nel dominio: {{self.data}}"
'''
