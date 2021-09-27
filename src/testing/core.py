class Expression:
    def __repr__(self):
        return f"{type(self).__name__}()"

    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return ""


class Operand(Expression):
    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return ""


class Operator(Expression):
    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return ""


class TrueOperand(Operand):
    def evaluate(self, assign: dict):
        return True

    def stringify(self, variables: dict):
        return "V"


class FalseOperand(Operand):
    def evaluate(self, assign: dict):
        return False

    def stringify(self, variables: dict):
        return "F"


class VarOperand(Operand):
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return f"{type(self).__name__}({self.var})"

    def evaluate(self, assign: dict):
        return assign[self.var]

    def stringify(self, variables: dict):
        return variables[self.var]


class UnaryOperator(Operator):
    def __init__(self, operand: Expression):
        self.operand = operand

    def __repr__(self):
        return f"{type(self).__name__}({self.operand})"

    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return self.operand.stringify(variables)


class NegateOperator(UnaryOperator):
    def __init__(self, operand: Expression):
        super().__init__(operand)

    def evaluate(self, assign: dict):
        return not self.operand.evaluate(assign)

    def stringify(self, variables: dict):
        return f"!{self.operand.stringify(variables)}"


class BinaryOperator(Operator):
    def __init__(self, lhs: Expression, rhs: Expression):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return f"{type(self).__name__}({self.lhs}, {self.rhs})"

    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return f"({self.lhs.stringify(variables)} {self.rhs.stringify(variables)})"


class AndOperator(BinaryOperator):
    def __init__(self, lhs: Expression, rhs: Expression):
        super().__init__(lhs, rhs)

    def evaluate(self, assign: dict):
        return self.lhs.evaluate(assign) and self.rhs.evaluate(assign)

    def stringify(self, variables: dict):
        return f"({self.lhs.stringify(variables)} & {self.rhs.stringify(variables)})"


class OrOperator(BinaryOperator):
    def __init__(self, lhs: Expression, rhs: Expression):
        super().__init__(lhs, rhs)

    def evaluate(self, assign: dict):
        return self.lhs.evaluate(assign) or self.rhs.evaluate(assign)

    def stringify(self, variables: dict):
        return f"({self.lhs.stringify(variables)} | {self.rhs.stringify(variables)})"


class ImplicationOperator(BinaryOperator):
    def __init__(self, lhs: Expression, rhs: Expression):
        super().__init__(lhs, rhs)

    def evaluate(self, assign: dict):
        return not self.lhs.evaluate(assign) or self.rhs.evaluate(assign)

    def stringify(self, variables: dict):
        return f"({self.lhs.stringify(variables)} -> {self.rhs.stringify(variables)})"


class EquivalenceOperator(BinaryOperator):
    def __init__(self, lhs: Expression, rhs: Expression):
        super().__init__(lhs, rhs)

    def evaluate(self, assign: dict):
        return not self.lhs.evaluate(assign) == self.rhs.evaluate(assign)

    def stringify(self, variables: dict):
        return f"({self.lhs.stringify(variables)} <-> {self.rhs.stringify(variables)})"
