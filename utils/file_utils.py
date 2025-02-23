# utils/file_utils.py
from pathlib import Path

def create_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Creata directory: {path}")

def write_file(path: Path, content: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[INFO] Creato file: {path}")

def create_init(directory: Path):
    init_file = directory / '__init__.py'
    if not init_file.exists():
        write_file(init_file, "")

def read_file(path: Path) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
