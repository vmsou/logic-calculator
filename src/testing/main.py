from solver import parse


def generate_variables(expr_vars):
    length = len(expr_vars)
    size = length
    vars_table = []

    if length:
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


def main():
    expr = "!p | p"
    res = parse(expr)
    op = res["op"]
    v = res["variables"]
    repeat_dict = {k: k for k in v}
    table = generate_variables(v)

    print(op.stringify(repeat_dict))
    for var in table:
        print(op.evaluate(var))


if __name__ == '__main__':
    main()
