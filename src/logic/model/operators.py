"""
Nesta seção é modelado os operados unários e binários.
"""

from logic.model import Operator, Expression, simplify
from logic.model.operands import TRUE, FALSE, VAR

"""Operadores unários"""
class UNARY(Operator):
    """Representa um Operador unário."""

    def __init__(self, operand: Expression):
        super().__init__()
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

    def variables(self):
        return self.operand.variables()


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
        op_type = self.operand.type

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
        super().__init__()
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.left}, {self.right})"

    def __eq__(self, other: Expression):
        if issubclass(type(other), BINARY):
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

    def variables(self):
        t = {}
        t.update(self.left.variables())
        t.update(self.right.variables())
        return t


class AND(BINARY):
    """Representa um Operador binário de conjunção."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def __eq__(self, other):
        if self.type == type(other):
            return (self.left == other.left and self.right == other.right) or (self.left == other.right and self.right == other.left)
        return False

    def evaluate(self, assign: dict) -> bool:
        return self.left.evaluate(assign) and self.right.evaluate(assign)

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()
        return f"({self.left.stringify(variables)} ∧ {self.right.stringify(variables)})"

    def simplify(self) -> Expression:
        # Idempotentes
        if self.left == self.right:
            return self.left.simplify()

        elif TRUE in (self.left.type, self.right.type):
            return self.left.simplify() if self.left.type != TRUE else self.right.simplify()

        elif self.is_false():
            return FALSE()

        # Absorção
        if self.right.type == OR and self.left in (self.right.left, self.right.right):
            return self.left

        elif self.left.type == OR and self.right in (self.left.left, self.left.right):
            return self.right

        # Associativa
        elif self.right.type == AND:
            # Idempotentes
            if self.left == self.right.left:
                return AND(self.left, self.right.right).simplify()
            elif self.left == self.right.right:
                return AND(self.left, self.right.left).simplify()
            # Contradição
            elif self.right.left.type == NOT and self.right.left.operand == self.left:
                return AND(FALSE(), self.right.right).simplify()
            elif self.right.right.type == NOT and self.right.right.operand == self.left:
                return AND(FALSE(), self.right.left).simplify()

        elif self.left.type == AND:
            if self.right == self.left.left:
                return AND(self.right, self.left.right).simplify()
            elif self.right == self.left.right:
                return AND(self.right, self.left.left).simplify()
            elif self.left.left.type == NOT and self.left.left.operand == self.right:
                return AND(self.left.right, FALSE()).simplify()
            elif self.left.right.type == NOT and self.left.right.operand == self.right:
                return AND(self.left.left, FALSE()).simplify()

        return super().simplify()

    def is_false(self):
        if FALSE in (self.left.type, self.right.type):
            return True

        elif self.right.type == NOT and self.left == self.right.operand:
            return True

        elif self.left.type == NOT and self.left.operand == self.right:
            return True

        return False


class OR(BINARY):
    """Representa um Operador binário de disjunção."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def __eq__(self, other):
        if self.type == type(other):
            return (self.left == other.left and self.right == other.right) or (self.left == other.right and self.right == other.left)
        return False

    def evaluate(self, assign: dict = None) -> bool:
        if assign is None:
            assign = dict()

        return self.left.evaluate(assign) or self.right.evaluate(assign)

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()

        return f"({self.left.stringify(variables)} ∨ {self.right.stringify(variables)})"

    def simplify(self) -> Expression:

        # Idempotentes
        if self.left == self.right:
            return self.left.simplify()

        elif self.is_true():
            return TRUE()

        elif FALSE in (self.left.type, self.right.type):
            return self.left.simplify() if self.left.type != FALSE else self.right.simplify()

        # Absorção
        elif self.right.type == AND and self.left in (self.right.left, self.right.right):
            return self.left.simplify()

        elif self.left.type == AND and self.right in (self.left.left, self.left.right):
            return self.right.simplify()

        # Associativa
        elif self.right.type == OR:
            if self.left == self.right.left:
                return OR(OR(self.left, self.right.left), self.right.right).simplify()
            elif self.left == self.right.right:
                return OR(OR(self.left, self.right.right), self.right.left).simplify()
            # Negado (esquerda)
            elif self.left.type == NOT:
                if self.left.operand == self.right.left:
                    return OR(OR(self.left, self.right.left), self.right.right).simplify()
                if self.left.operand == self.right.right:
                    return OR(OR(self.left, self.right.right), self.right.left).simplify()
            # Negado (direita)
            elif self.right.left.type == NOT and self.left == self.right.left.operand:
                return OR(OR(self.left, self.right.left), self.right.right)
            elif self.right.right.type == NOT and self.left == self.right.right.operand:
                return OR(OR(self.left, self.right.right), self.right.left)

        return super().simplify()

    def is_true(self):
        # Tautologia
        if TRUE in (self.left.type, self.right.type):
            return True
        elif self.left.type == NOT and self.left.operand == self.right:
            return True
        elif self.right.type == NOT and self.left == self.right.operand:
            return True
        elif self.left.type == NOT and self.left.operand == self.right:
            return True

        return False


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

    def simplify(self) -> Expression:
        return self.normalize().simplify()


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

    def simplify(self) -> Expression:
        return self.normalize().simplify()


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

    def simplify(self) -> Expression:
        return self.normalize().simplify()


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

    def simplify(self) -> Expression:
        return self.normalize().simplify()


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
    op = OR(VAR('A'), NOT(VAR('A')))
    op2 = OR(NOT(VAR('A')), OR(NOT(VAR('B')), VAR('A')))
    op3 = AND(VAR('A'), NOT(NOT(VAR('A'))))
    print(op3.stringify(dict()))
    print(simplify(op3).stringify())
    print(OR(VAR('A'), VAR('B')) == OR(VAR('A'), VAR('B')))
    print()


if __name__ == '__main__':
    # main()
    test()
