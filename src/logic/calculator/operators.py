from logic.calculator.core import Operator, Expression
from logic.calculator.operands import TRUE, FALSE

"""Operadores unários"""
class UnaryOperator(Operator):
    """Representa um Operador unário."""

    def __init__(self, operand: Expression):
        self.operand = operand

    def __repr__(self):
        return f"{type(self).__name__}({self.operand})"

    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return self.operand.stringify(variables)


class NOT(UnaryOperator):
    """Representa um Operador unário de negação."""

    def __init__(self, operand: Expression):
        super().__init__(operand)

    def evaluate(self, assign: dict):
        return not self.operand.evaluate(assign)

    def stringify(self, variables: dict):
        return f"(¬{self.operand.stringify(variables)})"

    def equivalences(self):
        equiv = [
            NAND(self.operand, self.operand),
            NOR(self.operand, self.operand)
        ]
        return equiv


"""Operadores binários"""
class BinaryOperator(Operator):
    """Representa um Operador binário."""

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{type(self).__name__}({self.left}, {self.right})"

    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} {self.right.stringify(variables)})"

    def equivalences(self):
        return []


class AND(BinaryOperator):
    """Representa um Operador binário de conjunção."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return self.left.evaluate(assign) and self.right.evaluate(assign)

    def stringify(self, variables: dict = None):
        if variables is None:
            variables = dict()
        return f"({self.left.stringify(variables)} ∧ {self.right.stringify(variables)})"

    def simplify(self, assign: dict = None):
        if assign is None:
            assign = dict()

        if FALSE in (type(self.left), type(self.right)):

            return FALSE()
        return self


class OR(BinaryOperator):
    """Representa um Operador binário de disjunção."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict = None):
        if assign is None:
            assign = dict()

        return self.left.evaluate(assign) or self.right.evaluate(assign)

    def stringify(self, variables: dict = None):
        if variables is None:
            variables = dict()

        return f"({self.left.stringify(variables)} ∨ {self.right.stringify(variables)})"

    def simplify(self, assign: dict = None):
        if assign is None:
            assign = dict()

        if TRUE in (type(self.left), type(self.right)):
            return TRUE()
        return self


class IMPLIES(BinaryOperator):
    """Representa um Operador binário de implicação."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return not self.left.evaluate(assign) or self.right.evaluate(assign)

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} → {self.right.stringify(variables)})"

    def simplify(self, assign: dict):
        return OR(NOT(self.left), self.right)

    def equivalences(self):
        equiv = [
            OR(NOT(self.left), self.right),
            NOT(AND(self.left, NOT(self.right)))
        ]
        return equiv


class EQUIVALENCE(BinaryOperator):
    """Representa um Operador binário de equivalência."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return self.left.evaluate(assign) == self.right.evaluate(assign)

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} ⟷ {self.right.stringify(variables)})"

    def equivalences(self):
        equiv = [
            AND(EQUIVALENCE(self.left, self.right), EQUIVALENCE(self.right, self.left)),
        ]
        return equiv


class NAND(BinaryOperator):
    """Representa um Operador binário de negação de conjunção."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return not (self.left.evaluate(assign) and self.right.evaluate(assign))

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} ↑ {self.right.stringify(variables)})"

    def equivalences(self):
        equiv = [
            NOT(AND(self.left, self.right)),
            OR(NOT(self.left), NOT(self.right))
        ]
        return equiv


class NOR(BinaryOperator):
    """Representa um Operador binário de negação de disjunção."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return not (self.left.evaluate(assign) or self.right.evaluate(assign))

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} ↓ {self.right.stringify(variables)})"

    def equivalences(self):
        equiv = [
            NOT(OR(self.left, self.right)),
            AND(NOT(self.left), NOT(self.right))
        ]
        return equiv


class XOR(BinaryOperator):
    """Representa um Operador binário de disjunção exclusiva."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return not (self.left.evaluate(assign) == self.right.evaluate(assign))

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} ⊻ {self.right.stringify(variables)})"

    def equivalences(self):
        equiv = [
            NOT(EQUIVALENCE(self.left, self.right)),
            AND(OR(self.left, self.right), NOT(AND(self.left, self.right)))
        ]
        return equiv