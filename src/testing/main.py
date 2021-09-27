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


def gen_table(res):
    tokens = res["tokens"]
    header = [str(i.value) for i in tokens if i.value is not None]
    print(header)


def main():
    expr = "V & F -> F & F -> V"
    parsed = parse(expr)
    v = parsed["variables"]
    op = parsed["op"]

    var_dict = {k: k for k in v}
    print(op.stringify(var_dict))

    res = op.evaluate(dict)
    print(res)

    # gen_table(parse(expr))


if __name__ == '__main__':
    main()
