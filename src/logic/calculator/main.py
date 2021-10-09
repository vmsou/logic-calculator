import sys

from logic.calculator.parser import LogicParser

errors = []

def header():
    size = 60
    print(" [Calculadora Lógica] ".center(size, '-'))
    print("Constantes: ")
    print("True = 'V', False = 'F'")
    print("Operadores Unários: ")
    print("NOT = '!'")
    print("Operadores Binários: ")
    print("AND = '&', OR = '|', IMPLICATION = '->', EQUIVALENCE = '<->'\n")
    print("-" * size)

def show_errors():
    for error in errors:
        print(f"\033[91m[Error] {error}\033[0m")
    errors.clear()

def main():
    parser = LogicParser()
    header()
    while True:
        expr = input("> ")
        parser.expr = expr
        try:
            parser.parse()
        except Exception as e:
            errors.append(e)

        if parser.valid:
            print(f"Fórmula Válida: {parser.valid}")
            if parser.is_fbf():
                print(f"Fórmula Bem Formada (FBF): Verdade")
            else:
                print(f"Fórmula Bem Formada (FBF): Falso")

            parser.show_table()

        show_errors()
        print(flush=True)


if __name__ == "__main__":
    main()
