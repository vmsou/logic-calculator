"""Basic Templates"""


class Expression:
    def __repr__(self):
        return f"{type(self).__name__}()"

    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return ""
    
    def simplify(self, assign: dict):
        return None


class Operand(Expression):
    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return ""
    
    def simplify(self, assign: dict):
        return None


class Operator(Expression):
    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return ""
    
    def simplify(self, assign: dict):
        return None


"""Constants"""


class TrueOperand(Operand):
    def evaluate(self, assign: dict):
        return True

    def stringify(self, variables: dict):
        return "V"
    
    def simplify(self, assign: dict):
        return True


class FalseOperand(Operand):
    def evaluate(self, assign: dict):
        return False

    def stringify(self, variables: dict):
        return "F"
    
    def simplify(self, assign: dict):
        return False


class VarOperand(Operand):
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return f"{type(self).__name__}({self.var})"

    def evaluate(self, assign: dict):
        return assign[self.var]

    def stringify(self, variables: dict):
        return variables[self.var]
    
    def simplify(self, assign: dict):
        return assign[self.var]


"""Unary Operators"""


class UnaryOperator(Operator):
    def __init__(self, operand: Expression):
        self.operand = operand

    def __repr__(self):
        return f"{type(self).__name__}({self.operand})"

    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return self.operand.stringify(variables)
    
    def simplify(self, assign: dict):
        return None


class NotOperator(UnaryOperator):
    def __init__(self, operand: Expression):
        super().__init__(operand)

    def evaluate(self, assign: dict):
        return not self.operand.evaluate(assign)

    def stringify(self, variables: dict):
        return f"¬{self.operand.stringify(variables)}"
    
    def simplify(self, assign: dict):
        return self

    def equivalences(self):
        equiv = [
            NotOperator(AndOperator(self.operand, self.operand)),
            NotOperator(OrOperator(self.operand, self.operand))
        ]
        return equiv


"""Binary Operators"""


class BinaryOperator(Operator):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{type(self).__name__}({self.left}, {self.right})"

    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} {self.right.stringify(variables)})"


class AndOperator(BinaryOperator):
    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return self.left.evaluate(assign) and self.right.evaluate(assign)

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} ∧ {self.right.stringify(variables)})"


class OrOperator(BinaryOperator):
    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return self.left.evaluate(assign) or self.right.evaluate(assign)

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} ∨ {self.right.stringify(variables)})"


class ImplicationOperator(BinaryOperator):
    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return not self.left.evaluate(assign) or self.right.evaluate(assign)

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} → {self.right.stringify(variables)})"

    def simplify(self, assign: dict):
        return OrOperator(NotOperator(self.left), self.right)

    def equivalences(self):
        equiv = [
            OrOperator(NotOperator(self.left), self.right),
            NotOperator(AndOperator(self.left, NotOperator(self.right)))
        ]
        return equiv


class EquivalenceOperator(BinaryOperator):
    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return not self.left.evaluate(assign) == self.right.evaluate(assign)

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} ⟷ {self.right.stringify(variables)})"

    def equivalences(self):
        equiv = [
            AndOperator(EquivalenceOperator(self.left, self.right), EquivalenceOperator(self.right, self.left)),
        ]
        return equiv


class NandOperator(BinaryOperator):
    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return not (self.left.evaluate(assign) and self.right.evaluate(assign))

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} ↑ {self.right.stringify(variables)})"

    def equivalences(self):
        equiv = [
            NotOperator(AndOperator(self.left, self.right)),
            OrOperator(NotOperator(self.left), NotOperator(self.right))
        ]
        return equiv
