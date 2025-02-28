#!/usr/bin/env python3
import argparse
import os
from core.module_generator.generator import ModuleGenerator
from core.dev_server import DevServer
from core.build_tool import BuildTool
from core.class_adder import ClassAdder

class QuarTrendCLI:
    @staticmethod
    def generate_module(args):
        is_main = (len(args.optional) >= 1 and args.optional[0].lower() == "main")
        socket_enabled = (len(args.optional) >= 2 and args.optional[1].lower() == "socket")
        base = args.base if args.base else "."
        gen = ModuleGenerator(args.module_name, base, is_main=is_main, socket_enabled=socket_enabled)
        gen.generate()

    @staticmethod
    def run_dev(args):
        module_path = args.module_path if args.module_path else os.getcwd()
        dev = DevServer(module_path)
        dev.start()

    @staticmethod
    def run_build(args):
        module_path = args.module_path if args.module_path else os.getcwd()
        builder = BuildTool(module_path)
        builder.build()

    @staticmethod
    def add_class(args):
        module_path = args.module_path if args.module_path else os.getcwd()
        url_prefix = args.optional[0] if len(args.optional) >= 1 else None
        subtype = args.optional[1] if len(args.optional) >= 2 else None
        prefix = args.optional[2] if len(args.optional) >= 3 else None
        adder = ClassAdder()
        adder.add(args.component_type, args.class_name, module_path, url_prefix, subtype, prefix)

def main():
    parser = argparse.ArgumentParser(
        description="QuarTrend CLI: genera moduli, avvia il server in sviluppo, esegue build e aggiunge componenti avanzati.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen_parser = subparsers.add_parser("generate", help="Genera un nuovo modulo")
    gen_parser.add_argument("module_name", type=str, help="Nome del modulo da creare")
    gen_parser.add_argument("base", type=str, nargs="?", default=".", help="Directory base per il modulo (default: '.')")
    gen_parser.add_argument("optional", nargs="*", help="Opzionali: 'main' per modulo principale, 'socket' per abilitare socket")
    gen_parser.set_defaults(func=QuarTrendCLI.generate_module)

    dev_parser = subparsers.add_parser("dev", help="Avvia l'app in modalità sviluppo")
    dev_parser.add_argument("module_path", type=str, nargs="?", default=None,
                            help="Percorso del modulo (default: directory corrente se esiste 'main.py')")
    dev_parser.set_defaults(func=QuarTrendCLI.run_dev)

    build_parser = subparsers.add_parser("build", help="Esegue la build per la produzione")
    build_parser.add_argument("module_path", type=str, nargs="?", default=None,
                              help="Percorso del modulo da buildare (default: directory corrente)")
    build_parser.set_defaults(func=QuarTrendCLI.run_build)

    add_parser = subparsers.add_parser("add", help="Aggiunge un nuovo componente (controller, service, model, template, endpoint o db)")
    add_parser.add_argument("component_type", type=str, choices=["controller", "service", "model", "template", "endpoint", "db"],
                            help="Tipo di componente da aggiungere.")
    add_parser.add_argument("class_name", type=str, help="Nome della classe/template da aggiungere")
    add_parser.add_argument("module_path", type=str, nargs="?", default=None,
                            help="Percorso della directory del modulo (default: directory corrente)")
    add_parser.add_argument("optional", nargs="*", help="Opzionali: url_prefix, subtype, prefix (in quest'ordine)")
    add_parser.set_defaults(func=QuarTrendCLI.add_class)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
