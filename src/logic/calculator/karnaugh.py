from logic.calculator.parser import LogicParser
from logic.calculator.table import TruthTable
from logic.model.operators import *

def karnaugh2(header, data):
    length = 2
    found = []

    s0 = data[3][length]
    s1 = data[2][length]
    s2 = data[1][length]
    s3 = data[0][length]

    v = ('V', 'V')

    if (s0, s1) == v:
        found.append(NOT(VAR(header[1])))
    if (s2, s3) == v:
        found.append(VAR(header[0]))
    if (s0, s1) == v:
        found.append(NOT(VAR(header[0])))
    if (s1, s3) == v:
        found.append(VAR(header[1]))
    return found


def karnaugh3(header, data):
    length = 3
    found = []

    s0 = data[7][length]
    s1 = data[6][length]
    s2 = data[5][length]
    s3 = data[4][length]
    s4 = data[3][length]
    s5 = data[2][length]
    s6 = data[1][length]
    s7 = data[0][length]

    v = ('V', 'V')

    # Linhas
    if (s0, s2) == v:
        a = NOT(VAR(header[0]))
        b = NOT(VAR(header[2]))
        found.append(AND(a, b))

    if (s1, s3) == v:
        a = NOT(VAR(header[0]))
        b = VAR(header[2])
        found.append(AND(a, b))

    if (s4, s6) == v:
        a = VAR(header[0])
        b = NOT(VAR(header[2]))
        found.append(AND(a, b))

    if (s5, s7) == v:
        a = VAR(header[0])
        b = VAR(header[1])
        found.append(AND(a, b))

    # Colunas
    if (s0, s4) == v:
        a = NOT(VAR(header[1]))
        b = NOT(VAR(header[2]))
        found.append(AND(a, b))

    if (s1, s5) == v:
        a = NOT(VAR(header[1]))
        b = VAR(header[2])
        found.append(AND(a, b))

    if (s3, s7) == v:
        a = VAR(header[1])
        b = VAR(header[2])
        found.append(AND(a, b))

    if (s2, s6) == v:
        a = VAR(header[1])
        b = NOT(VAR(header[2]))
        found.append(AND(a, b))

    return found


def karnaugh(table: TruthTable):
    length = len(table.variables.keys())
    header, data = table.generate()

    found = []
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
