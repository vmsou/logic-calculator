from src.core.stream import cin, ts
from src.core.exceptions import ExpectedToken, PrimaryExpected


def primary():
    """Retorna o resultado numérico de uma expressão ou termo"""
    t = ts.get()
    if t.kind == '!':
        return not expression()

    elif t.kind == '(':
        val = expression()
        t = ts.get()
        if t.kind != ')':
            raise ExpectedToken(f"Token expected: ')'")
        return val

    elif t.kind == 'c':
        return bool(t.value)
    else:
        raise PrimaryExpected(f"Primary Expected but got {t}")


def term():
    """Retorna o resultado de uma operação involvendo multiplicação, divisão, e/ou o valor"""
    left = primary()
    t = ts.get()

    while True:
        if t.kind == '->':
            left *= primary()
            t = ts.get()
        elif t.kind == '<->':
            pass
        else:
            ts.putback(t)
            return left


def expression():
    """Retorna o resultado de uma operação matematica envolvendo seus termos, adições e subtrações"""
    left = term()
    t = ts.get()

    while True:
        if t.kind == '&':
            left &= term()
            t = ts.get()
        elif t.kind == '|':
            left |= term()
            t = ts.get()
        else:
            ts.putback(t)
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
