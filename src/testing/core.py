class Node:
    def __repr__(self):
        return f"{type(self).__name__}()"

    def evaluate(self, assign):
        return None

    def stringify(self, variables):
        return ""


class Operand(Node):
    def evaluate(self, assign):
        return None

    def stringify(self, variables):
        return ""


class TrueOperand(Operand):
    def evaluate(self, assign):
        return True

    def stringify(self, variables):
        return "V"


class FalseOperand(Operand):
    def evaluate(self, assign):
        return False

    def stringify(self, variables):
        return "F"


class VarOperand(Operand):
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return f"{type(self).__name__}({self.var})"

    def evaluate(self, assign):
        return assign[self.var]

    def stringify(self, variables):
        return variables[self.var]


class UnaryOperand(Operand):
    def __init__(self, operand: Operand):
        self.operand = operand

    def __repr__(self):
        return f"{type(self).__name__}({self.operand})"

    def evaluate(self, assign):
        return None

    def stringify(self, variables):
        return self.operand.stringify(variables)


class NegateOperand(UnaryOperand):
    def __init__(self, operand: Operand):
        super().__init__(operand)

    def evaluate(self, assign):
        return not self.operand.evaluate(assign)

    def to_string(self, variables):
        return "!" + self.operand.stringify(variables)


class BinaryOperand(Operand):
    def __init__(self, lhs: Operand, rhs: Operand):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return f"{type(self).__name__}({self.lhs}, {self.rhs})"

    def evaluate(self, assign):
        return None

    def stringify(self, variables):
        return f"({self.lhs.stringify(variables)} {self.rhs.stringify(variables)})"


class AndOperand(BinaryOperand):
    def __init__(self, lhs: Operand, rhs: Operand):
        super().__init__(lhs, rhs)

    def evaluate(self, assign):
        return self.lhs.evaluate(assign) and self.rhs.evaluate(assign)

    def stringify(self, variables):
        return f"({self.lhs.stringify(variables)} & {self.rhs.stringify(variables)})"


class OrOperand(BinaryOperand):
    def __init__(self, lhs: Operand, rhs: Operand):
        super().__init__(lhs, rhs)

    def evaluate(self, assign):
        return self.lhs.evaluate(assign) or self.rhs.evaluate(assign)

    def stringify(self, variables):
        return f"({self.lhs.stringify(variables)} | {self.rhs.stringify(variables)})"


class ImplicationOperand(BinaryOperand):
    def __init__(self, lhs: Operand, rhs: Operand):
        super().__init__(lhs, rhs)

    def evaluate(self, assign):
        return not self.lhs.evaluate(assign) or self.rhs.evaluate(assign)

    def stringify(self, variables):
        return f"({self.lhs.stringify(variables)} -> {self.rhs.stringify(variables)})"


class EquivalenceOperand(BinaryOperand):
    def __init__(self, lhs: Operand, rhs: Operand):
        super().__init__(lhs, rhs)

    def evaluate(self, assign):
        return not self.lhs.evaluate(assign) == self.rhs.evaluate(assign)

    def stringify(self, variables):
        return f"({self.lhs.stringify(variables)} <-> {self.rhs.stringify(variables)})"
