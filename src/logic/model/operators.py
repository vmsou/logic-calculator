"""
Nesta seção é modelado os operados unários e binários.
"""

from logic.model import Operator, Expression
from logic.model.operands import TRUE, FALSE, VAR

"""Operadores unários"""
class UNARY(Operator):
    """Representa um Operador unário."""

    def __init__(self, operand: Expression):
        self.operand = operand

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.operand})"

    def __eq__(self, other: Expression):
        if issubclass(type(other), UNARY):
            return super().__eq__(other) and self.operand == other.operand
        return False

    def evaluate(self, assign: dict) -> bool:
        return True

    def stringify(self, variables: dict) -> str:
        return self.operand.stringify(variables)

    def normalize(self):
        return type(self)(self.operand.normalize())

    def simplify(self):
        return type(self)(self.operand.simplify())


class NOT(UNARY):
    """Representa um Operador unário de negação."""

    def __init__(self, operand: Expression):
        super().__init__(operand)

    def evaluate(self, assign: dict) -> bool:
        return not self.operand.evaluate(assign)

    def stringify(self, variables: dict) -> str:
        return f"(¬{self.operand.stringify(variables)})"

    def equivalences(self) -> list:
        return [
            NAND(self.operand, self.operand),
            NOR(self.operand, self.operand)
        ]

    def simplify(self) -> Expression:
        op_type = type(self.operand)

        if op_type == NOT:
            return self.operand.operand.simplify()
        elif op_type == TRUE:
            return FALSE()
        elif op_type == FALSE:
            return TRUE()

        return super().simplify()


"""Operadores binários"""
class BINARY(Operator):
    """Representa um Operador binário."""

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.left}, {self.right})"

    def __eq__(self, other: Expression):
        type_other = type(other)
        if issubclass(type_other, BINARY):
            return super().__eq__(other) and self.left == other.left and self.right == other.right
        return False

    def evaluate(self, assign: dict) -> bool:
        return True

    def stringify(self, variables: dict) -> str:
        return f"({self.left.stringify(variables)} {self.right.stringify(variables)})"

    def equivalences(self) -> list:
        return []

    def normalize(self):
        return type(self)(self.left.normalize(), self.right.normalize())

    def simplify(self) -> Expression:
        return type(self)(self.left.simplify(), self.right.simplify())


class AND(BINARY):
    """Representa um Operador binário de conjunção."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict) -> bool:
        return self.left.evaluate(assign) and self.right.evaluate(assign)

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()
        return f"({self.left.stringify(variables)} ∧ {self.right.stringify(variables)})"

    def simplify(self) -> Expression:
        if FALSE in (type(self.left), type(self.right)):
            return FALSE()
        return super().simplify()


class OR(BINARY):
    """Representa um Operador binário de disjunção."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict = None) -> bool:
        if assign is None:
            assign = dict()

        return self.left.evaluate(assign) or self.right.evaluate(assign)

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()

        return f"({self.left.stringify(variables)} ∨ {self.right.stringify(variables)})"

    def simplify(self) -> Expression:
        left_op = type(self.left)
        right_op = type(self.right)

        if self.left == self.right:
            return self.left.simplify()
        elif TRUE in (left_op, right_op):
            return TRUE()
        elif FALSE in (left_op, right_op):
            return self.left.simplify() if left_op != FALSE else self.right.simplify()

        return super().simplify()


class IMPLY(BINARY):
    """Representa um Operador binário de implicação."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict) -> bool:
        return not self.left.evaluate(assign) or self.right.evaluate(assign)

    def stringify(self, variables: dict) -> str:
        return f"({self.left.stringify(variables)} → {self.right.stringify(variables)})"

    def equivalences(self) -> list:
        return [
            OR(NOT(self.left), self.right),
            NOT(AND(self.left, NOT(self.right)))
        ]

    def normalize(self):
        return OR(NOT(self.left), self.right).normalize()

    def simplify(self) -> Expression:
        return self.normalize().simplify()


class EQUAL(BINARY):
    """Representa um Operador binário de equivalência."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict) -> bool:
        return self.left.evaluate(assign) == self.right.evaluate(assign)

    def stringify(self, variables: dict) -> str:
        return f"({self.left.stringify(variables)} ⟷ {self.right.stringify(variables)})"

    def equivalences(self) -> list:
        return [
            AND(IMPLY(self.left, self.right), IMPLY(self.right, self.left)),
        ]

    def normalize(self):
        return AND(IMPLY(self.left, self.right), IMPLY(self.right, self.left)).normalize()


class NAND(BINARY):
    """Representa um Operador binário de negação de conjunção."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict) -> bool:
        return not (self.left.evaluate(assign) and self.right.evaluate(assign))

    def stringify(self, variables: dict) -> str:
        return f"({self.left.stringify(variables)} ↑ {self.right.stringify(variables)})"

    def equivalences(self) -> list:
        return [
            NOT(AND(self.left, self.right)),
            OR(NOT(self.left), NOT(self.right))
        ]

    def normalize(self):
        return NOT(AND(self.left, self.right)).normalize()


class NOR(BINARY):
    """Representa um Operador binário de negação de disjunção."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict) -> bool:
        return not (self.left.evaluate(assign) or self.right.evaluate(assign))

    def stringify(self, variables: dict) -> str:
        return f"({self.left.stringify(variables)} ↓ {self.right.stringify(variables)})"

    def equivalences(self) -> list:
        return [
            NOT(OR(self.left, self.right)),
            AND(NOT(self.left), NOT(self.right))
        ]

    def normalize(self):
        return NOT(OR(self.left, self.right)).normalize()


class XOR(BINARY):
    """Representa um Operador binário de disjunção exclusiva."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict) -> bool:
        return not (self.left.evaluate(assign) == self.right.evaluate(assign))

    def stringify(self, variables: dict) -> str:
        return f"({self.left.stringify(variables)} ⊻ {self.right.stringify(variables)})"

    def equivalences(self) -> list:
        return [
            NOT(EQUAL(self.left, self.right)),
            AND(OR(self.left, self.right), NOT(AND(self.left, self.right)))
        ]

    def normalize(self):
        # return NOT(EQUAL(self.left, self.right)).normalize()
        return AND(OR(self.left, self.right), NOT(AND(self.left, self.right))).normalize()


def main() -> None:
    op1: Expression = IMPLY(AND(VAR('A'), VAR('B')), FALSE())
    op2: Expression = EQUAL(VAR('A'), VAR('B'))
    op3: Expression = XOR(VAR('A'), VAR('B'))

    ops = [op1, op2, op3]

    for op in ops:
        print(op.stringify(dict()), end=' = ')
        print(op.evaluate(dict()))
        print("Normalized")
        canon_op = op.normalize()
        print(canon_op.stringify(dict()), end=' = ')
        print(canon_op.evaluate(dict()))
        print()

    print("\nSimplificação: ")
    op1: Expression = NOT(NOT(AND(TRUE(), FALSE())))
    op2: Expression = IMPLY(NOT(NOT(TRUE())), FALSE())

    ops = [op1, op2]

    for op in ops:
        print(op.stringify(dict()))
        print(op.simplify().stringify(dict()))
        print()

def test():
    op = OR(VAR('q'), FALSE())
    print(op.stringify(dict()))
    print(op.simplify().stringify(dict()))
    print()


if __name__ == '__main__':
    # main()
    test()
