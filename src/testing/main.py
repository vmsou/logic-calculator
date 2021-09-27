from solver import parse
from core import current


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

    print(op.stringify(repeat_dict), '\n')
    for var in table:
        print(var)
        current.clear()
        op.evaluate(var)
        for k, v in current.items():
            print(k, v, sep=' ')
        print()


def gen_table(res):
    tokens = res["tokens"]
    header = [str(i.value) for i in tokens if i.value is not None]
    print(header)


def main():
    expr = "p -> q & r"
    calculate(expr)



if __name__ == '__main__':
    main()
