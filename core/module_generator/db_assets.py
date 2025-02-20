from pathlib import Path
from utils.file_utils import write_file

def generate_db_assets(base_path: Path, module_name: str):
    db_dir = base_path / "db"
    # Assicurati che la directory esista (già creata in create_directories)
    db_manager_code = f'''"""
Questo file definisce un semplice ORM per il modulo {module_name}.
Utilizzo:
    - La classe DBManager implementa l’interfaccia IDatabase e gestisce le operazioni di base.
"""

from interfaces.db import IDatabase

class DBManager(IDatabase):
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.connection = None

    def connect(self):
        self.connection = f"Connected to {{self.db_url}}"
        print(f"[DB] {{self.connection}}")

    def disconnect(self):
        print("[DB] Disconnected")
        self.connection = None

    def execute(self, query: str, params: dict = None):
        print(f"[DB] Executing query: {{query}} with params: {{params}}")
        return []
'''
    write_file(db_dir / "db_manager.py", db_manager_code)
