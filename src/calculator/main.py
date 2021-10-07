from logic_parser import Parser


def main():
    parser = Parser()
    while True:
        parser.set_expr(input("> "))
        parser.parse()
        if parser.valid:
            parser.show_table()
        print()


if __name__ == "__main__":
    main()
