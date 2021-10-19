from logic.calculator.parser import LogicParser
from logic.calculator.table import TruthTable
from logic.stream.core import logic_map, Logic

ONLY_CANON: bool = False
SIMPLIFY: bool = False

def header() -> None:
    """Imprime o cabeçalho do programa. Mostra simbolos permitidos."""
    size: int = 60
    print("[ Calculadora Lógica ]".center(size, '-'))
    print("Constantes: ")
    print(f"TRUE = {logic_map[Logic.TRUE]}\nFALSE = {logic_map[Logic.FALSE]}")
    print(f"VAR = {logic_map[Logic.VAR]}")
    print("-" * 20)
    print("Operadores Unários: ")
    print(f"NOT = {logic_map[Logic.NOT]}")
    print("-" * 20)
    print("Operadores Binários: ")
    print(f"AND = {logic_map[Logic.AND]}")
    print(f"OR = {logic_map[Logic.OR]}")
    if not ONLY_CANON:
        print(f"IMPLY = {logic_map[Logic.IMPLY]}")
        print(f"EQUAL = {logic_map[Logic.EQUAL]}")
        print(f"XOR = {logic_map[Logic.XOR]}")
        print(f"NOR = {logic_map[Logic.NOR]}")
        print(f"NAND = {logic_map[Logic.NAND]}")
    print("-" * size)

def show_errors(errors: list[Exception]) -> None:
    """Imprime uma lista de erros e depois limpa a lista."""
    for error in errors:
        print(f"\033[91m[Error] {error}\033[0m")
    errors.clear()

def options():
    global ONLY_CANON, SIMPLIFY

    if input("Permitir somente canônicas (s/n): ").lower() in ('s', 'sim', 'si', 'y', 'yes'):
        ONLY_CANON = True

    if input("Mostrar simbolos permitidos (s/n): ").lower() in ('s', 'sim', 'si', 'y', 'yes'):
        header()

    if input("Simplificar (Não completo) (s/n): ").lower() in ('s', 'sim', 'si', 'y', 'yes'):
        SIMPLIFY = True

def main() -> None:
    options()
    print()

    errors: list[Exception] = []
    parser: LogicParser = LogicParser(normalize=ONLY_CANON, simplify_expression=SIMPLIFY)
    while True:
        parser.expr = input("> ")
        try:
            parser.parse()
        except Exception as e:
            errors.append(e)

        print(f"Fórmula Válida: {parser.is_valid()}")
        if parser.is_valid():
            table: TruthTable = parser.get_table()
            print(f"Fórmula Canônica: {parser.is_canon()}")
            table.show()

        show_errors(errors)
        print(flush=True)


if __name__ == "__main__":
    main()
