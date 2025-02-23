"""
Questo file definisce un modello di dominio per il modulo {MODULE_NAME}.
Scopo: Rappresentare le entità e la logica di business inerente ai dati.
Utilizzo:
    - Il modello gestisce dati e li elabora tramite il metodo process.
"""

from interfaces.business import IModel

class SampleModel(IModel):
    def __init__(self, data):
        self.data = data

    def process(self):
        return f"Elaborazione dati da SampleModel: {{self.data}}"
