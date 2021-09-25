from src.core.stream import InputStream, TokenStream, Logic, logicMap
from src.core.exceptions import ExpectedToken, PrimaryExpected

cin = InputStream(input)
ts = TokenStream(cin)

variables = {}

truth_str = {True: "V", False: "F"}
truth_bool = {"V": True, "F": False}


def define_var(var, value):
    variables[var] = value


def primary():
    """Retorna o resultado booleano de uma expressão ou termo"""
    t = ts.get()
    if t.kind == Logic.NOT:
        return not expression()

    elif t.kind == Logic.OPEN:
        val = expression()
        t = ts.get()
        if t.kind != Logic.CLOSE:
            raise ExpectedToken(f"Token expected: ')'")
        return val

    elif t.kind == Logic.VAR:
        return bool(variables[t.value])

    elif t.kind == Logic.CONSTANT:
        return bool(t.value)
    else:
        raise PrimaryExpected(f"Primary Expected but got {t}")


def term():
    """Retorna o resultado de uma operação involvendo multiplicação, divisão, e/ou o valor"""
    left = primary()
    t = ts.get()

    while True:
        if t.kind == Logic.IMPLICATION:
            right = primary()
            if not left:
                left = True
            elif left and right:
                left = True
            else:
                left = False
            t = ts.get()
        elif t.kind == Logic.EQUIVALENCE:
            right = primary()
            if left and right:
                left = True
            elif not left and not right:
                left = True
            else:
                left = False
            t = ts.get()
        else:
            ts.putback(t)
            return left


def expression():
    """Retorna o resultado de uma operação matematica envolvendo seus termos, AND e OR"""
    left = term()
    t = ts.get()

    while True:
        if t.kind == Logic.AND:
            left &= term()
            t = ts.get()
        elif t.kind == Logic.OR:
            left |= term()
            t = ts.get()
        elif t.kind == Logic.CONSTANT:
            raise ExpectedToken('Illegal:' + t.value)
        elif t.kind == Logic.OPEN:
            raise ExpectedToken('Illegal: ' + t.value)
        else:
            ts.putback(t)
            return left


def get_variables(expr: str):
    sample_vars = logicMap[Logic.VAR]
    found_vars = set()
    for i in expr:
        if i in sample_vars:
            found_vars.add(i)
    return sorted(found_vars)


def generate_variables(expr_vars):
    length = len(expr_vars)
    size = length
    vars_table = {}

    if length:
        size = 2 ** length
        half = size

        for var in expr_vars:
            curr_vars = []
            half //= 2
            actual = True
            for j in range(1, size + 1):
                curr_vars.append(truth_str[actual])
                if j % half == 0:
                    actual = not actual
            vars_table[var] = curr_vars
    return vars_table, size


def result():
    try:
        return expression()
    except Exception as e:
        print("[Error]", e)
        ts.clean()


def update_variables(vars_values, row):
    vars_names = []
    for var in vars_values:
        value = vars_values[var][row]
        define_var(var, truth_bool[value])
        vars_names.append(value)
    return vars_names


def calculate(expr):
    expr_vars = get_variables(expr)
    vars_values, size = generate_variables(expr_vars)

    if size:
        print(" ".join(expr_vars), "\t", expr)
        for row in range(size):
            cin.buffer = expr
            vars_names = update_variables(vars_values, row)
            print(" ".join(vars_names), end='\t')
            res = result()
            print("\t", truth_str[res])
    else:
        print(expr)
        res = result()
        if res is not None:
            print(truth_str[res])


def main():
    print("Constantes: ")
    print("True = 'V', False = 'F'")
    print("Operadores Unários: ")
    print("NOT = '!'")
    print("Operadores Binários: ")
    print("AND = '&', OR = '|', IMPLICATION = '->', EQUIVALENCE = '<->'\n")

    while True:
        print(">", end=' ')
        cin.input()
        calculate(cin.buffer)
        print()


if __name__ == '__main__':
    main()








