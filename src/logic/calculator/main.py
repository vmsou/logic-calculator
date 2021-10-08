import sys

from logic.calculator.parser import LogicParser


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
        parser.expr = input("> ")
        try:
            parser.parse()
            print(f"Fórmula Bem Formada (FBF): {parser.is_fbf()}")
        except Exception as e:
            print(f"\nError: {e}\n", file=sys.stderr)
        if parser.valid:
            parser.show_table()
        print()


if __name__ == "__main__":
    main()
