from typing import Optional, Any

from src.core.exceptions import ParseError, BadToken
from src.core.stream import Logic, Token
from core import *
from verify import setup

operator_map = {
    Logic.AND: AndOperator,
    Logic.OR: OrOperator,
    Logic.EQUIVALENCE: EquivalenceOperator,
    Logic.IMPLICATION: ImplicationOperator
}


def parse(expr: str) -> dict[str, Any]:
    setup_result: dict[str, Optional[Operand, dict]] = setup(expr)
    tokens: list[Token] = setup_result["tokens"]

    operators: list[Token] = []
    operands: list[Operand] = []

    expect_operand = True

    for t in tokens:
        if expect_operand:
            if t.kind in (Logic.CONSTANT, Logic.VAR):
                add_operand(to_operand(t), operands, operators)
                expect_operand = False
            elif t.kind == Logic.OPEN or t.kind == Logic.NOT:
                operators.append(t)
            elif t.kind == Logic.EOF:
                if len(operators) == 0:
                    raise ParseError("Erro de Parse")
                elif last(operators).kind == Logic.OPEN:
                    raise ParseError(f"Parêntese aberto não possui fechamento {operators}.")

                raise ParseError(f"Falta operandos para esse operadores {operators}.")
            else:
                raise ParseError("Esperava variável, constante, ou parênteses.")
        else:
            if t.kind in (Logic.AND, Logic.OR, Logic.IMPLICATION, Logic.EQUIVALENCE, Logic.EOF):
                while True:
                    if len(operators) == 0:
                        break
                    if last(operators).kind == Logic.OPEN:
                        break

                    if priority(last(operators)) < priority(t):
                        break

                    operator: Token = operators.pop()
                    rhs: Operand = operands.pop()
                    lhs: Operand = operands.pop()

                    add_operand(to_operator(lhs, operator, rhs), operands, operators)

                operators.append(t)
                expect_operand = True
                if t.kind == Logic.EOF:
                    break

            elif t.kind == Logic.CLOSE:
                while True:
                    if len(operators) == 0:
                        raise ParseError(f"Não possui parêntese de abertura {t}.")
                    curr_op: Token = operators.pop()

                    if curr_op.kind == Logic.OPEN:
                        break
                    if curr_op.kind == Logic.NOT:
                        raise ParseError("Nenhum operando para negar.", curr_op)

                    rhs: Operand = operands.pop()
                    lhs: Operand = operands.pop()

                    add_operand(to_operator(lhs, curr_op, rhs), operands, operators)

                ex: Operand = operands.pop()
                add_operand(ex, operands, operators)
            else:
                raise ParseError(f"Esperando parêntese de fechada {t}.")

    assert len(operators) != 0
    assert operators.pop().kind == Logic.EOF

    if len(operators) != 0:
        mismatched_op: Token = operators.pop()
        assert mismatched_op.kind == Logic.OPEN
        raise ParseError(f"Nenhum parêntese de fechamento {mismatched_op}.")

    return dict(tokens=tokens, operand=operands.pop(), vars=setup_result["vars"])


def to_operand(token: Token) -> Operand:
    if token.kind == Logic.CONSTANT:
        if token.value:
            return TrueOperand()
        elif not token.value:
            return FalseOperand()
    elif token.kind == Logic.VAR:
        return VarOperand(token.value)
    raise BadToken(f"{token} não é um operando.")


def to_operator(lhs: Operand, token: Token, rhs: Operand) -> Operator:
    if token.kind in operator_map:
        return operator_map[token.kind](lhs, rhs)
    raise BadToken(f"{token} não é um operador.")


def add_operand(expr: Expression, operands, operators):
    while len(operators) > 0 and last(operators).kind == Logic.NOT:
        operators.pop()
        expr = NegateOperator(expr)

    operands.append(expr)


def last(tokens: list):
    length = len(tokens)
    assert length != 0
    return tokens[length - 1]


def priority(token: Token):
    return token.kind.value


def main():
    expr = "p | q"
    res = parse(expr)
    op: Operand = res["operand"]
    print(op)


if __name__ == '__main__':
    main()
