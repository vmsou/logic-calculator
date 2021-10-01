from table import calculate, show_table


def main():
    while True:
        expr = input("> ")
        table = calculate(expr)
        show_table(table)
        print()


if __name__ == "__main__":
    main()
