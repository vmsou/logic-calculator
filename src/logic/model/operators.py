"""
Nesta seção é modelado os operados unários e binários.
"""

from logic.model import Operator, Expression, ANY
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
        if type(other) == ANY:
            return True
        elif issubclass(type(other), UNARY):
            return super().__eq__(other) and self.operand == other.operand
        return False

    def __iter__(self):
        yield self.operand

    def evaluate(self, assign: dict = None) -> bool:
        return True

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()
        return self.operand.stringify(variables)

    def normalize(self):
        return type(self)(self.operand.normalize())

    def simplify(self):
        return type(self)(self.operand.simplify())

    def variables(self):
        return self.operand.variables()

    def find(self, predicate):
        """Retorna o elemento com tipo igual e um diferente"""
        if predicate(self.operand.type):
            return self.operand, None
        return None, None


class NOT(UNARY):
    """Representa um Operador unário de negação."""

    def __init__(self, operand: Expression):
        super().__init__(operand)

    def evaluate(self, assign: dict = None) -> bool:
        if assign is None:
            assign = dict()
        return not self.operand.evaluate(assign)

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()
        return f"¬{self.operand.stringify(variables)}"

    def equivalences(self) -> list:
        return [
            NAND(self.operand, self.operand),
            NOR(self.operand, self.operand)
        ]

    def simplify(self) -> Expression:
        if self.operand.type == NOT:
            return self.operand.operand.simplify()
        elif self.operand.type == TRUE:
            return FALSE()
        elif self.operand.type == FALSE:
            return TRUE()

        return super().simplify()

    def negated(self) -> Expression:
        return self.operand.negated()


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
        if type(other) == ANY:
            return True
        elif issubclass(type(other), BINARY):
            return super().__eq__(other) and self.left == other.left and self.right == other.right
        return False

    def __iter__(self):
        yield self.left
        yield self.right

    def evaluate(self, assign: dict = None) -> bool:
        return True

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()
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

    def find(self, predicate):
        """Retorna o elemento com tipo igual e um diferente"""
        found, not_found = None, None
        found = next(filter(predicate, self))
        for i in self:
            if not predicate(i):
                not_found = i
        return found, not_found


class AND(BINARY):
    """Representa um Operador binário de conjunção."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def __eq__(self, other):
        if type(other) == ANY:
            return True
        elif self.type == type(other):
            return (self.left == other.left and self.right == other.right) or (self.left == other.right and self.right == other.left)
        return False

    def evaluate(self, assign: dict = None) -> bool:
        if assign is None:
            assign = dict()
        return self.left.evaluate(assign) and self.right.evaluate(assign)

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()
        return f"({self.left.stringify(variables)} ∧ {self.right.stringify(variables)})"

    def simplify(self) -> Expression:
        # Idempotentes
        if self.left == self.right:
            return self.left.simplify()

        elif self.left == NOT(self.right.negated().simplify()):
            return self.right.simplify()
        elif self.right == NOT(self.left.negated().simplify()):
            return self.left.simplify()

        elif TRUE() in self:
            not_true = next(filter(lambda x: x != TRUE(), self))
            return not_true.simplify()

        elif self.is_false():
            return FALSE()

        # Absorção
        elif self == AND(self.left, OR(self.left, ANY())):
            return self.left.simplify()
        elif self == AND(self.right, OR(self.right, ANY())):
            return self.right.simplify()

        # Associativa p ^ (p ^ q) == (p ^ p) ^ q
        elif self == AND(self.left, AND(self.left, ANY())):
            found_AND, not_AND = self.find(lambda x: x.type == AND)
            AND_not_left, _ = found_AND.find(lambda x: x != not_AND)
            return AND(not_AND, AND_not_left).simplify()

        # Associativa (p ^ q) ^ q == p ^ (q ^ q)
        elif self == AND(self.right, AND(self.right, ANY())):
            found_AND, not_AND = self.find(lambda x: x.type == AND)
            AND_not_right, _ = found_AND.find(lambda x: x != not_AND)
            return AND(AND_not_right, not_AND).simplify()

        return super().simplify()

    def is_false(self):
        if FALSE() in self:
            return True
        elif self == AND(NOT(self.left), self.left):
            return True
        elif self == AND(NOT(self.right), self.right):
            return True

        # Associativa
        elif self.left.type == self.type:
            if NOT(self.right) in self.left:
                return True
            for i in self.left:
                if NOT(i) == self.right:
                    return True
        elif self.right.type == self.type:
            if NOT(self.left) in self.right:
                return True
            for i in self.right:
                if NOT(i) == self.left:
                    return True
        return False

    def negated(self) -> Expression:
        return OR(NOT(self.left), NOT(self.right))


class OR(BINARY):
    """Representa um Operador binário de disjunção."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def __eq__(self, other):
        if type(other) == ANY:
            return True
        elif self.type == type(other):
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

        elif self.left == NOT(self.right.negated().simplify()):
            return self.right.simplify()
        elif self.right == NOT(self.left.negated().simplify()):
            return self.left.simplify()

        # Tautologia
        elif self.is_true():
            return TRUE()

        # Neutro
        elif FALSE() in self:
            return self.left.simplify() if self.left.type != FALSE else self.right.simplify()

        # Absorção
        elif self == OR(self.left, AND(self.left, ANY())):
            return self.left.simplify()
        elif self == OR(self.right, AND(self.right, ANY())):
            return self.right.simplify()

        # Associativa p v (p v q) == (p v p) v q
        elif self == OR(self.left, OR(self.left, ANY())):
            found_or, not_or = self.find(lambda x: x.type == OR)
            or_not_left, _ = found_or.find(lambda x: x != not_or)
            return OR(not_or, or_not_left).simplify()

        # Associativa (p v q) v q == p v (q v q)
        elif self == OR(self.right, OR(self.right, ANY())):
            found_or, not_or = self.find(lambda x: x.type == OR)
            or_not_left, _ = found_or.find(lambda x: x != not_or)
            return OR(or_not_left, not_or).simplify()

        return super().simplify()

    def is_true(self):
        # Tautologia
        if TRUE() in self:
            return True
        elif self == OR(NOT(self.right), self.right):
            return True
        elif self == OR(NOT(self.left), self.left):
            return True

        # Associativa
        elif self.left.type == OR:
            if NOT(self.right) in self.left:
                return True
            for i in self.left:
                if NOT(i) == self.right:
                    return True
        elif self.right.type == OR:
            if NOT(self.left) in self.right:
                return True
            for i in self.right:
                if NOT(i) == self.left:
                    return True

        return False

    def negated(self) -> Expression:
        return AND(NOT(self.left), NOT(self.right))


class IMPLY(BINARY):
    """Representa um Operador binário de implicação."""

    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict = None) -> bool:
        if assign is None:
            assign = dict()
        return not self.left.evaluate(assign) or self.right.evaluate(assign)

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()
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

    def evaluate(self, assign: dict = None) -> bool:
        if assign is None:
            assign = dict()
        return self.left.evaluate(assign) == self.right.evaluate(assign)

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()
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

    def evaluate(self, assign: dict = None) -> bool:
        if assign is None:
            assign = dict()
        return not (self.left.evaluate(assign) and self.right.evaluate(assign))

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()
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

    def evaluate(self, assign: dict = None) -> bool:
        if assign is None:
            assign = dict()
        return not (self.left.evaluate(assign) or self.right.evaluate(assign))

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()
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

    def evaluate(self, assign: dict = None) -> bool:
        if assign is None:
            assign = dict()
        return not (self.left.evaluate(assign) == self.right.evaluate(assign))

    def stringify(self, variables: dict = None) -> str:
        if variables is None:
            variables = dict()
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
    op1: Expression = OR(VAR('p'), VAR('q'))
    print(op1.stringify())
    print(op1.negated().simplify().stringify())
    print(op1.evaluate())


if __name__ == '__main__':
    main()
