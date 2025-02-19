# quargen.py
#!/usr/bin/env python3
import argparse
from core.module_generator.generator import ModuleGenerator
from core.dev_server import DevServer
from core.build_tool import BuildTool
from core.class_adder import ClassAdder

class QuarTrendCLI:
    @staticmethod
    def generate_module(args):
        gen = ModuleGenerator(args.name, args.base, is_main=args.main, socket_enabled=args.socket)
        gen.generate()

    @staticmethod
    def run_dev(args):
        dev = DevServer(args.module)
        dev.start()

    @staticmethod
    def run_build(args):
        builder = BuildTool(args.module)
        builder.build()

    @staticmethod
    def add_class(args):
        adder = ClassAdder()
        # Il flag --prefix viene usato sia per i template che per gli endpoint
        adder.add(args.type, args.class_name, args.module, getattr(args, 'url_prefix', None), getattr(args, 'subtype', None), getattr(args, 'prefix', None))

def main():
    parser = argparse.ArgumentParser(
        description="QuarTrend CLI: genera moduli articolati, avvia il server in sviluppo, esegue build e aggiunge componenti avanzati.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Comando generate
    gen_parser = subparsers.add_parser("generate", help="Genera un nuovo modulo")
    gen_parser.add_argument("--name", type=str, required=True, help="Nome del modulo da creare")
    gen_parser.add_argument("--base", type=str, default=".", help="Directory base per il modulo")
    gen_parser.add_argument("--main", action="store_true", help="Indica che il modulo è il principale (usa endpoint '/')")
    gen_parser.add_argument("--socket", action="store_true", help="Abilita il supporto socket per il modulo")
    gen_parser.set_defaults(func=QuarTrendCLI.generate_module)

    # Comando dev
    dev_parser = subparsers.add_parser("dev", help="Avvia l'app in modalità sviluppo")
    dev_parser.add_argument("--module", type=str, default=".", help="Percorso del modulo (directory contenente main.py)")
    dev_parser.set_defaults(func=QuarTrendCLI.run_dev)

    # Comando build
    build_parser = subparsers.add_parser("build", help="Esegue la build per la produzione")
    build_parser.add_argument("--module", type=str, required=True, help="Percorso del modulo da buildare")
    build_parser.set_defaults(func=QuarTrendCLI.run_build)

    # Comando add: estendiamo le tipologie supportate includendo anche "endpoint"
    add_parser = subparsers.add_parser("add", help="Aggiunge un nuovo componente (controller, service, model, template o endpoint)")
    add_parser.add_argument("--type", type=str, choices=["controller", "service", "model", "template", "endpoint"], required=True,
                            help="Tipo di componente da aggiungere. 'endpoint' permette di creare un nuovo endpoint API aggiuntivo.")
    add_parser.add_argument("--class_name", type=str, required=True, help="Nome della classe/template da aggiungere")
    add_parser.add_argument("--module", type=str, required=True, help="Percorso della directory del modulo")
    add_parser.add_argument("--url_prefix", type=str, default=None,
                            help="(Opzionale, per template) URL prefix per l'endpoint da generare")
    add_parser.add_argument("--subtype", type=str, default=None,
                            help="Sottotipo per il componente (per controller: rest, web; per service: business, data; per model: domain, dto)")
    # Aggiungiamo il flag --prefix per gli endpoint
    add_parser.add_argument("--prefix", type=str, default=None,
                            help="(Opzionale, per endpoint) Prefisso per l'endpoint API, ad esempio 'extra' per generare '/api/<modulo>/extra'")
    add_parser.set_defaults(func=QuarTrendCLI.add_class)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
