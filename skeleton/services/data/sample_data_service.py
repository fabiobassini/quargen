"""
Questo file definisce un service per l'accesso ai dati per il modulo {MODULE_NAME}.
Scopo: Recuperare i dati necessari.
"""

from interfaces.data import IDataAccess

class SampleDataService(IDataAccess):
    def get_data(self):
        return "Dati ottenuti da SampleDataService"
