"""
Nesta seção é modelado os operados unários e binários.
"""

from logic.model import Operator, Expression, ANY, simplify
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

    def find(self, expr_type):
        """Retorna o elemento com tipo igual e um diferente"""
        if self.operand.type == expr_type:
            return self.operand, None
        return None, None


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

    def negated(self) -> Expression:
        return type(self)(self.left.negated(), self.right.negated())

    def variables(self):
        t = {}
        t.update(self.left.variables())
        t.update(self.right.variables())
        return t

    def find(self, expr_type):
        """Retorna o elemento com tipo igual e um diferente"""
        if self.left.type == expr_type:
            return self.left, self.right
        elif self.right.type == expr_type:
            return self.right, self.left
        return None, None


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

        elif TRUE() in self:
            _, not_true = self.find(TRUE)
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
            found_and, not_or = self.find(AND)
            and_not_left = found_and.left if found_and.left != not_or else found_and.right
            return AND(not_or, and_not_left).simplify()

        # Associativa (p ^ q) ^ q == p ^ (q ^ q)
        elif self == AND(self.right, AND(self.right, ANY())):
            found_and, not_or = self.find(AND)
            and_not_right = found_and.left if found_and.left != not_or else found_and.right
            return AND(and_not_right, not_or).simplify()

        return super().simplify()

    def negated(self) -> Expression:
        return OR(self.left.negated(), self.right.negated())

    def is_false(self):
        if FALSE() in self:
            return True
        elif self == AND(NOT(self.left), self.left):
            return True
        elif self == AND(NOT(self.right), self.right):
            return True

        return False


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
            found_or, not_or = self.find(OR)
            or_not_left = found_or.left if found_or.left != not_or else found_or.right
            return OR(not_or, or_not_left).simplify()

        # Associativa (p v q) v q == p v (q v q)
        elif self == OR(self.right, OR(self.right, ANY())):
            found_or, not_or = self.find(OR)
            or_not_right = found_or.left if found_or.left != not_or else found_or.right
            return OR(or_not_right, not_or).simplify()

        # Associativa ~p v (p v q) == (~p v p) v q == V v q == V
        elif self.left.type == NOT and self == OR(NOT(self.left.operand), OR(self.left.operand, ANY())):
            found_or, not_or = self.find(OR)
            _, or_not_left = found_or.find(self.left.type)
            return TRUE()

        # Associativa (p v q) v ~p == q v (p v ~p) == q v V == V
        elif self.right.type == NOT and self == OR(OR(self.right.operand, ANY()), NOT(self.right.operand)):
            found_or, not_or = self.find(OR)
            _, or_not_right = found_or.find(self.right.type)
            return TRUE()

        return super().simplify()

    def negated(self) -> Expression:
        return AND(self.left.negated(), self.right.negated())

    def is_true(self):
        # Tautologia
        if TRUE() in self:
            return True
        elif self == OR(NOT(self.right), self.right):
            return True
        elif self == OR(NOT(self.left), self.left):
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
    print(OR(TRUE(), FALSE()) == OR(ANY(), TRUE()))
    print(VAR('q') == ANY())
    print(OR(VAR('p'), OR(VAR('p'), VAR('q'))) == OR(OR(VAR('p'), VAR('q')), VAR('p')))
    not_negated = NOT(OR(NOT(VAR('A')), VAR('B')))
    negated = not_negated.negated()
    print(not_negated.stringify(dict()))
    print(negated.stringify(dict()))


if __name__ == '__main__':
    # main()
    test()
