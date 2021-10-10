from logic.calculator.parser import LogicParser

def header():
    size = 60
    print("[ Calculadora Lógica ]".center(size, '-'))
    print("Constantes: ")
    print("True = 'V', False = 'F'")
    print("Operadores Unários: ")
    print("NOT = '!'")
    print("Operadores Binários: ")
    print("AND = '&', OR = '|', IMPLICATION = '->', EQUIVALENCE = '<->'")
    print("Variáveis: p, q, r, A, B e C")
    print("-" * size)

def show_errors(errors):
    for error in errors:
        print(f"\033[91m[Error] {error}\033[0m")
    errors.clear()

def main():
    errors: list[Exception] = []
    parser = LogicParser()
    header()
    while True:
        parser.expr = input("> ")
        try:
            parser.parse()
        except Exception as e:
            errors.append(e)

        print(f"Fórmula Válida: {parser.is_valid()}")
        if parser.is_valid():
            print(f"Fórmula Bem Formada (FBF): {parser.is_fbf()}")
            parser.show_table()

        show_errors(errors)
        print(flush=True)


if __name__ == "__main__":
    main()
