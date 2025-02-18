#!/usr/bin/env python3
import os
import re
import argparse

# Definiamo dei pattern per identificare le funzioni/entrypoint da considerare come moduli.
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

def generate_aggregator(aggregated_analysis, output_path):
    """
    Genera uno skeleton di file aggregator che raccoglie i moduli individuati in tutte le repository analizzate.
    Nel file vengono commentate le parti trovate in ciascuna repo per facilitare l'integrazione manuale.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Aggregator per la registrazione dei moduli provenienti da repository multiple\n")
            f.write("from flask import Flask\n\n")
            f.write("app = Flask(__name__)\n\n")
            f.write("# Moduli identificati dall'analisi (da integrare manualmente):\n")
            for repo, analysis in aggregated_analysis.items():
                f.write(f"# Repository: {repo}\n")
                for file, entries in analysis.items():
                    f.write(f"#   File: {file}\n")
                    for entry in entries:
                        tipo, line_number, snippet = entry
                        f.write(f"#     [{tipo}] Line {line_number}: {snippet}\n")
                f.write("\n")
            f.write("def register_modules(app):\n")
            f.write("    # TODO: Importa ed integra i moduli individuati\n")
            f.write("    # Esempio:\n")
            f.write("    # from modulo_a import ModuleA\n")
            f.write("    # module_a = ModuleA()\n")
            f.write("    # app.register_blueprint(module_a.get_api_blueprint())\n")
            f.write("    # app.register_blueprint(module_a.get_ui_blueprint())\n")
            f.write("    pass\n\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    register_modules(app)\n")
            f.write("    app.run(port=5000)\n")
        print(f"Skeleton aggregator generato in: {output_path}")
    except Exception as e:
        print(f"Errore nella generazione del file aggregator: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Tool da linea di comando per analizzare più repository e generare uno skeleton aggregator."
    )
    parser.add_argument('--repos', type=str, nargs='+', required=True,
                        help="Percorsi delle repository da analizzare (uno o più)")
    parser.add_argument('--output', type=str,
                        help="File di output per il report dell'analisi aggregata (opzionale)")
    parser.add_argument('--generate-aggregator', type=str,
                        help="Percorso del file da generare come skeleton aggregator (opzionale)")
    
    args = parser.parse_args()

    aggregated_analysis = {}
    # Analizza ogni repository e raccoglie i risultati in un dizionario
    for repo in args.repos:
        print(f"\nAnalizzo la repository: {repo}")
        analysis = analyze_repo(repo)
        aggregated_analysis[repo] = analysis
        print_analysis(analysis)
    
    # Se specificato, scrive un report aggregato in un file
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as out_file:
                for repo, analysis in aggregated_analysis.items():
                    out_file.write(f"Repository: {repo}\n")
                    for file, entries in analysis.items():
                        out_file.write(f"  File: {file}\n")
                        for entry in entries:
                            tipo, line_number, snippet = entry
                            out_file.write(f"    [{tipo}] Line {line_number}: {snippet}\n")
                    out_file.write("\n")
            print(f"\nReport aggregato scritto in: {args.output}")
        except Exception as e:
            print(f"Errore nello scrivere il report: {e}")
    
    # Genera lo skeleton del file aggregator se richiesto
    if args.generate_aggregator:
        generate_aggregator(aggregated_analysis, args.generate_aggregator)

if __name__ == '__main__':
    main()
