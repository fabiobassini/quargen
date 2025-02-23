from pathlib import Path

def replace_placeholder_in_files(directory: Path, placeholder: str, replacement: str):
    for path in directory.rglob("*"):
        if path.is_file():
            try:
                content = path.read_text(encoding="utf-8")
            except Exception:
                continue
            new_content = content.replace(placeholder, replacement)
            path.write_text(new_content, encoding="utf-8")
