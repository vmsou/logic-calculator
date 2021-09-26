from src.core.stream import Logic, Token
from core import *
from verify import check


def parse(expr):
    check_result = check(expr)
    tokens = check_result["tokens"]

    operators = []
    operands = []

    expect_operand = True

    for t in tokens:
        if expect_operand:
            if t.kind in (Logic.CONSTANT, Logic.VAR):
                add_operand(map_operand(t), operands, operators)
                expect_operand = False
            elif t.kind == Logic.OPEN or t.kind == Logic.NOT:
                operators.append(t)
            elif t.kind == Logic.EOF:
                if len(operators) == 0:
                    raise Exception()
                elif top_of(operators).kind == Logic.OPEN:
                    raise Exception("Open Parenthesis has no matching close parenthesis")




def map_operand(token: Token) -> Operand:
    if token.value == 'V': return TrueOperand()
    if token.value == 'F': return FalseOperand()
    if token.kind == Logic.VAR: return VarOperand(token.value)
    raise Exception(f"{token} não é um operando")


def add_operand(node: Node, operands, operators):
    while len(operators) > 0 and top_of(operators).kind != Logic.NOT:
        operators.pop()
        node = NegateNode(node)

    operands.append(node)

def top_of(arr):
    length = len(arr)
    assert length != 0
    return arr[length - 1]


if __name__ == '__main__':
    parse("p | q")