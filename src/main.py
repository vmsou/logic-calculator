from logic.calculator.parser import LogicParser
from logic.calculator.table import TruthTable
from logic.stream.core import logic_map, Logic

ONLY_CANON: bool = True

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
        print(f"IMPLIES = {logic_map[Logic.IMPLICATION]}")
        print(f"EQUIVALENCE = {logic_map[Logic.EQUIVALENCE]}")
        print(f"XOR = {logic_map[Logic.XOR]}")
        print(f"NOR = {logic_map[Logic.NOR]}")
        print(f"NAND = {logic_map[Logic.NAND]}")
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
            table: TruthTable = parser.get_table()
            print(f"Fórmula Canônica: {parser.is_canon()}")
            if ONLY_CANON:
                if parser.is_canon():
                    table.show()
            else:
                table.show()

        show_errors(errors)
        print(flush=True)


if __name__ == "__main__":
    main()
