from table import calculate, show_table
from core import ImplicationOperator, VarOperand


def main():
    func = ImplicationOperator(VarOperand("A"), VarOperand("B"))
    print(func.stringify(dict(A='A', B='B')))
    for f in func.equivalences():
        print(f.stringify(dict(A='A', B='B')))

    while True:
        expr = input("> ")
        table = calculate(expr)
        show_table(table)
        print()


if __name__ == "__main__":
    main()
