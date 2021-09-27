import tabulate

from solver import parse


def bool_to_str(boolean):
    if boolean:
        return "V"
    return "F"


def generate_variables(expr_vars):
    length = len(expr_vars)
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
    truth = generate_variables(v)

    header = [k for k in sorted(v)]
    header.append(op.stringify(repeat_dict))
    table = [header]

    for var in truth:
        row = [bool_to_str(var[key]) for key in sorted(var)]
        row.append(bool_to_str(op.evaluate(var)))
        table.append(row)

    return table


def gen_table(res):
    tokens = res["tokens"]
    header = [str(i.value) for i in tokens if i.value is not None]
    print(header)


def main():
    expr = "p -> q -> r & p"
    table = calculate(expr)

    print(tabulate.tabulate(table, tablefmt='fancy_grid', stralign='center'))


if __name__ == '__main__':
    main()
