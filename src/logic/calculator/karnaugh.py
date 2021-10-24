from logic.calculator.parser import LogicParser
from logic.calculator.table import TruthTable
from logic.model.operators import *


def karnaugh2(header: list[str], data: list[list[str]]) -> list[Expression]:
    length: int = 2
    found: list[Expression] = []

    s0: str = data[3][length]
    s1: str = data[2][length]
    s2: str = data[1][length]
    s3: str = data[0][length]

    v = ('V', 'V')

    a: Expression = VAR(header[0])
    b: Expression = VAR(header[1])

    # Linhas
    if (s0, s1) == v:
        found.append(NOT(a))
    if (s2, s3) == v:
        found.append(a)

    # Colunas
    if (s0, s2) == v:
        found.append(NOT(b))
    if (s1, s3) == v:
        found.append(b)
    return found


def karnaugh3(header: list[str], data: list[list[str]]) -> list[Expression]:
    length: int = 3
    found: list[Expression] = []

    def append(left: Expression, right: Expression) -> None:
        found.append(AND(left, right))

    s0: str = data[7][length]
    s1: str = data[6][length]
    s2: str = data[5][length]
    s3: str = data[4][length]
    s4: str = data[3][length]
    s5: str = data[2][length]
    s6: str = data[1][length]
    s7: str = data[0][length]

    v = ('V', 'V')

    a: Expression = VAR(header[0])
    b: Expression = VAR(header[1])
    c: Expression = VAR(header[2])

    # Linhas - a to c
    if (s0, s2) == v:
        x = NOT(a)
        y = NOT(c)
        append(x, y)

    if (s1, s3) == v:
        x = NOT(a)
        y = c
        append(x, y)

    if (s4, s6) == v:
        x = a
        y = NOT(c)
        append(x, y)

    if (s5, s7) == v:
        x = a
        y = c
        append(x, y)

    # Colunas - b to c
    if (s0, s4) == v:
        x = NOT(b)
        y = NOT(c)
        append(x, y)

    if (s1, s5) == v:
        x = NOT(b)
        y = c
        append(x, y)

    if (s3, s7) == v:
        x = b
        y = c
        append(x, y)

    if (s2, s6) == v:
        x = b
        y = NOT(c)
        append(x, y)

    return found


def karnaugh(table: TruthTable) -> Expression:
    length = len(table.variables.keys())
    header, data = table.generate()

    found: list[Expression] = []
    if length == 2:
        found = karnaugh2(header, data)
    if length == 3:
        found = karnaugh3(header, data)

    if len(found) == 1:
        return found[0]
    else:
        op = OR(found[0], found[1])

        for i in range(2, len(found)):
            op = OR(op, found[i])

        return op


def main() -> None:
    parser: LogicParser = LogicParser(simplify_expression=True)

    expr1 = "(A ∧ B) ∨ A"
    expr2 = "(¬A ∧ ¬B ∧ C) ∨ (¬A ∧ B ∧ C) ∨ (A ∧ ¬B ∧ ¬C) ∨ (A ∧ ¬B ∧ C) ∨ (A ∧ B ∧ ¬C)"

    parser.expr = expr2
    parser.parse()

    table: TruthTable = TruthTable(parser.expression)
    table.show()

    table.expression = karnaugh(table)
    table.show()


if __name__ == '__main__':
    main()
