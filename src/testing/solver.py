from typing import  Any

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
    setup_result = setup(expr)
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
                    raise ParseError(f"Parêntese aberto não possui fechamento para token: {t}.")

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
                    left: Operand = operands.pop()
                    right: Operand = operands.pop()

                    add_operand(to_operator(left, operator, right), operands, operators)

                operators.append(t)
                expect_operand = True
                if t.kind == Logic.EOF:
                    break

            elif t.kind == Logic.CLOSE:
                while True:
                    if len(operators) == 0:
                        raise ParseError(f"Não possui parêntese de abertura {t}.")
                    operator: Token = operators.pop()

                    if operator.kind == Logic.OPEN:
                        break
                    if operator.kind == Logic.NOT:
                        raise ParseError("Nenhum operando para negar.", operator)

                    left: Operand = operands.pop()
                    right: Operand = operands.pop()

                    add_operand(to_operator(left, operator, right), operands, operators)

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


def add_operand(ex: Expression, operands, operators):
    while len(operators) and last(operators).kind == Logic.NOT:
        operators.pop()
        ex = NegateOperator(ex)

    operands.append(ex)


def last(tokens: list):
    length = len(tokens)
    assert length != 0
    return tokens[length - 1]


def priority(token: Token):
    return token.kind.value


if __name__ == '__main__':
    expr = "p -> q"
    res = parse(expr)
    op: Operand = res["operand"]
    var: dict[str, bool] = res["vars"]
    print(op)
    print(var)
    print(op.evaluate(var))
