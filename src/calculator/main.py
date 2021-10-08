import sys

from logicParser import LogicParser
from stream.exceptions import ParseError


def header():
    print(" [Calculadora Lógica] ".center(60, '-'))
    print("Constantes: ")
    print("True = 'V', False = 'F'")
    print("Operadores Unários: ")
    print("NOT = '!'")
    print("Operadores Binários: ")
    print("AND = '&', OR = '|', IMPLICATION = '->', EQUIVALENCE = '<->'\n")


def main():
    parser = LogicParser()
    header()
    while True:
        expr = input("> ")
        parser.set_expr(expr)
        try:
            parser.parse()
        except Exception as e:
            print(f"Error: {e}\n", file=sys.stderr)
        if parser.valid:
            parser.show_table()
        print()


if __name__ == "__main__":
    main()
