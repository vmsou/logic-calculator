from solver import parse


def generate_variables(expr_vars):
    length = len(expr_vars)
    vars_table = []

    size = 2 ** length
    vars_table = [{} for _ in range(size)]
    half = size

    for var in expr_vars:
        half //= 2
        actual = True
        for j in range(1, size + 1):
            vars_table[j-1][var] = actual
            if j % half == 0:
                actual = not actual

    return vars_table


def calculate(expr):
    res = parse(expr)
    op = res["op"]
    v = res["variables"]
    repeat_dict = {k: k for k in v}
    table = generate_variables(v)

    print(op.stringify(repeat_dict))
    for var in table:
        print(op.stringify(var), end=' ')
        print(op.evaluate(var))


def main():
    expr = "q | !q -> p & !p"
    calculate(expr)


if __name__ == '__main__':
    main()
