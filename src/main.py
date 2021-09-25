from src.core.stream import cin, ts, Logic
from src.core.exceptions import ExpectedToken, PrimaryExpected


def primary():
    """Retorna o resultado numérico de uma expressão ou termo"""
    t = ts.get()
    if t.kind == Logic.NOT:
        return not expression()

    elif t.kind == Logic.OPEN:
        val = expression()
        t = ts.get()
        if t.kind != Logic.CLOSE:
            raise ExpectedToken(f"Token expected: ')'")
        return val

    elif t.kind == Logic.CONSTANT:
        return bool(t.value)
    else:
        raise PrimaryExpected(f"Primary Expected but got {t}")


def term():
    """Retorna o resultado de uma operação involvendo multiplicação, divisão, e/ou o valor"""
    left = primary()
    t = ts.get()

    while True:
        if t.kind == Logic.CONDITIONAL:
            left *= primary()
            t = ts.get()
        elif t.kind == Logic.BICONDITIONAL:
            pass
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
        else:
            return left


def main():
    print("Constantes: ")
    print("True = 'V', False = 'F'")
    print("Operadores Unários: ")
    print("NOT = '!'")
    print("Operadores Binários: ")
    print("AND = '&', OR = '|'\n")

    while True:
        print(">", end=' ')
        cin.input()
        try:
            res = expression()
            print("Resultado:", res)
        except Exception as e:
            print("[Error]", e)


if __name__ == '__main__':
    main()
