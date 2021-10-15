"""
Nesta seção é modelado os operados unários e binários.
"""

from logic.model import Operator, Expression
from logic.model.operand import TRUE, FALSE, VAR

"""Operadores unários"""
class Unary(Operator):
    """Representa um Operador unário."""

    def __init__(self, operand: Expression):
        self.operand = operand

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.operand})"

    def evaluate(self, assign: dict) -> bool:
        return True

    def stringify(self, variables: dict) -> str:
        return self.operand.stringify(variables)

    def normalize(self):
        return type(self)(self.operand.normalize())


class NOT(Unary):
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


"""Operadores binários"""
class Binary(Operator):
    """Representa um Operador binário."""

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.left}, {self.right})"

    def evaluate(self, assign: dict) -> bool:
        return True

    def stringify(self, variables: dict) -> str:
        return f"({self.left.stringify(variables)} {self.right.stringify(variables)})"

    def equivalences(self) -> list:
        return []

    def normalize(self):
        return type(self)(self.left.normalize(), self.right.normalize())


class AND(Binary):
    """Representa um Operador binário de conjunção."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict) -> bool:
        return self.left.evaluate(assign) and self.right.evaluate(assign)

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()
        return f"({self.left.stringify(variables)} ∧ {self.right.stringify(variables)})"

    def simplify(self, assign: dict = None) -> Expression:
        if assign is None:
            assign = dict()

        if FALSE in (type(self.left), type(self.right)):

            return FALSE()
        return self


class OR(Binary):
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

    def simplify(self, assign: dict = None) -> Expression:
        if assign is None:
            assign = dict()

        if TRUE in (type(self.left), type(self.right)):
            return TRUE()
        return self


class IMPLY(Binary):
    """Representa um Operador binário de implicação."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict) -> bool:
        return not self.left.evaluate(assign) or self.right.evaluate(assign)

    def stringify(self, variables: dict) -> str:
        return f"({self.left.stringify(variables)} → {self.right.stringify(variables)})"

    def simplify(self, assign: dict) -> Expression:
        return OR(NOT(self.left), self.right)

    def equivalences(self) -> list:
        return [
            OR(NOT(self.left), self.right),
            NOT(AND(self.left, NOT(self.right)))
        ]

    def normalize(self):
        return OR(NOT(self.left), self.right).normalize()


class EQUAL(Binary):
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


class NAND(Binary):
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


class NOR(Binary):
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


class XOR(Binary):
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


def main() -> None:
    op: Expression = IMPLY(AND(VAR('p'), VAR('q')), FALSE())
    print(op.stringify(dict()))
    print(op.evaluate(dict(p=False, q=False)))

    canon_op = op.normalize()
    print(canon_op.stringify(dict()))

    op2: Expression = EQUAL(VAR('A'), VAR('B'))
    canon_op2 = op2.normalize()
    print(op2.stringify(dict()))
    print(canon_op2.stringify(dict()))


if __name__ == '__main__':
    main()
