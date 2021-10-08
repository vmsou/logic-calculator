from logicParser import LogicParser


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
        parser.parse()
        if parser.valid:
            parser.show_table()
        print()


if __name__ == "__main__":
    main()
