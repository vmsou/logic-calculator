from src.core.exceptions import ParseError
from src.core.stream import Logic, Token
from core import *
from verify import check


def parse(expr):
    check_result = check(expr)
    tokens = check_result["tokens"]

    operators = []
    operands = []

    print(TrueOperand())

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
                    raise ParseError("Parse Error")
                elif top_of(operators).kind == Logic.OPEN:
                    raise ParseError("Open Parenthesis has no matching close parenthesis", operators)

                raise ParseError("This operators is missing an operand", operators)
            else:
                raise ParseError("Expecting a variable, constant or parenthesis here")
        else:
            if t.kind in (Logic.AND, Logic.OR, Logic.IMPLICATION, Logic.EQUIVALENCE, Logic.EOF):
                # Evaluate higher priority
                while True:
                    if len(operators) == 0: break
                    if top_of(operators).kind == Logic.OPEN: break
                    if priority(top_of(operators)) <= priority(t): break

                    operator = operators.pop()
                    rhs = operands.pop()
                    lhs = operands.pop()

                    add_operand(to_operator(lhs, operator, rhs), operands, operators)

                operators.append(t)
                expect_operand = True
                if t.kind == Logic.EOF: break

            elif t.kind == Logic.CLOSE:
                while True:
                    if len(operators) == 0:
                        raise ParseError("No matching open parenthesis", t)
                    curr_op = operators.pop()

                    if curr_op.kind == Logic.OPEN: break
                    if curr_op.kind == Logic.NOT:
                        raise ParseError("No operand to negate.", curr_op)

                    rhs = operands.pop()
                    lhs = operands.pop()

                    add_operand(to_operator(lhs, curr_op, rhs), operands, operators)

                ex = operands.pop()
                add_operand(ex, operands, operators)
            else:
                raise ParseError(f"Expecting close parenthesis. {curr_op}")

    assert len(operators) != 0
    assert operators.pop().kind == Logic.EOF

    if len(operators) != 0:
        mismatched_op = operators.pop()
        assert mismatched_op.kind == Logic.OPEN
        raise ParseError(f"No matching close parenthesis. {mismatched_op}")

    return dict(ast=operands.pop(), variables=check_result["variables"])


def to_operand(token: Token) -> Operand:
    if token.value: return TrueOperand()
    if not token.value: return FalseOperand()
    if token.kind == Logic.VAR: return VarOperand(token.value)
    raise Exception(f"{token} não é um operando")


def to_operator(lhs, token: Token, rhs) -> Operand:
    if token.kind == Logic.EQUIVALENCE: return EquivalenceOperand(lhs, rhs)
    if token.kind == Logic.IMPLICATION: return ImplicationOperand(lhs, rhs)
    if token.kind == Logic.OR: return OrOperand(lhs, rhs)
    if token.kind == Logic.AND: return AndOperand(lhs, rhs)
    raise Exception(f"{token} não é um operador")


def add_operand(node: Node, operands, operators):
    while len(operators) > 0 and top_of(operators).kind == Logic.NOT:
        operators.pop()
        node = NegateOperand(node)

    operands.append(node)


def top_of(arr):
    length = len(arr)
    assert length != 0
    return arr[length - 1]


def priority(token):
    return token.kind.value


if __name__ == '__main__':
    res = parse("(V & V) & V")
    op = res["ast"]
    print(op.evaluate("o"))
