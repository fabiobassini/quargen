# analysis/analyzer.py
import os
import re

PATTERNS = {
    "API": re.compile(r"def\s+get_api_blueprint\s*\("),
    "UI": re.compile(r"def\s+get_ui_blueprint\s*\("),
    "Socket": re.compile(r"def\s+handle_connection\s*\(")
}

def analyze_file(file_path):
    """
    Analizza un file Python e restituisce una lista di tuple (tipo, numero linea, snippet)
    per ogni riga che corrisponde a uno dei pattern definiti.
    """
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                for tipo, pattern in PATTERNS.items():
                    if pattern.search(line):
                        results.append((tipo, i + 1, line.strip()))
    except Exception as e:
        print(f"Errore nell'aprire {file_path}: {e}")
    return results

def analyze_repo(repo_path):
    """
    Scansiona ricorsivamente la directory della repository cercando file Python e applica analyze_file.
    Restituisce un dizionario dove la chiave è il percorso del file e il valore è la lista dei match trovati.
    """
    analysis = {}
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                file_results = analyze_file(file_path)
                if file_results:
                    analysis[file_path] = file_results
    return analysis

def print_analysis(analysis):
    """
    Stampa a schermo i risultati dell'analisi per una singola repository.
    """
    if not analysis:
        print("  Nessun pattern individuato in questa repository.")
        return
    for file, entries in analysis.items():
        print(f"  File: {file}")
        for entry in entries:
            tipo, line_number, snippet = entry
            print(f"    [{tipo}] Line {line_number}: {snippet}")
