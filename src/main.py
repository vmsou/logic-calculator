from logic.calculator.parser import LogicParser

ONLY_CANON: bool = True

def header() -> None:
    """Imprime o cabeçalho do programa. Mostra simbolos permitidos."""
    size: int = 60
    print("[ Calculadora Lógica ]".center(size, '-'))
    print("Constantes: ")
    print("True = 'V', False = 'F'")
    print("Operadores Unários: ")
    print("NOT = '!', '~'")
    print("Operadores Binários: ")
    print("AND = '&', OR = '|', IMPLICATION = '->', EQUIVALENCE = '<->'")
    print("Variáveis: p, q e r")
    print("-" * size)

def show_errors(errors: list[Exception]) -> None:
    """Imprime uma lista de erros e depois limpa a lista."""
    for error in errors:
        print(f"\033[91m[Error] {error}\033[0m")
    errors.clear()

def main() -> None:
    errors: list[Exception] = []
    parser: LogicParser = LogicParser()
    header()
    while True:
        parser.expr = input("> ")
        try:
            parser.parse()
        except Exception as e:
            errors.append(e)

        print(f"Fórmula Válida: {parser.is_valid()}")
        if parser.is_valid():
            print(f"Fórmula Canônica: {parser.is_canon()}")
            if ONLY_CANON:
                if parser.is_canon():
                    parser.show_table()
            else:
                parser.show_table()

        show_errors(errors)
        print(flush=True)


if __name__ == "__main__":
    main()
