"""
Questo file definisce un Data Transfer Object (DTO) per il modulo {MODULE_NAME}.
Scopo: Facilitare il trasferimento di dati tra i componenti.
"""

class SampleDTO:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def to_dict(self):
        return self.__dict__
