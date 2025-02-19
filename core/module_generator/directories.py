from pathlib import Path
from utils.file_utils import create_dir, create_init

def create_directories(base_path: Path):
    dirs = [
        base_path,
        base_path / "config",
        base_path / "docs",
        base_path / "models" / "domain",
        base_path / "models" / "dto",
        base_path / "controllers" / "rest",
        base_path / "controllers" / "web",
        base_path / "services" / "business",
        base_path / "services" / "data",
        base_path / "utils",
        base_path / "tests",
        base_path / "api",
        base_path / "ui",
        base_path / "sockets",
        base_path / "interfaces"
    ]
    for d in dirs:
        create_dir(d)
        create_init(d)
