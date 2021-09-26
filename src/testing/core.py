class Operator:
    def evaluate(self, assign):
        return None

    def stringify(self, variables):
        return ""


class TrueNode(Operator):
    def evaluate(self, assign):
        return True

    def stringify(self, variables):
        return "V"


class FalseNode(Operator):
    def evaluate(self, assign):
        return False

    def stringify(self, variables):
        return "F"


class UnaryOperator(Operator):
    def __init__(self, operand: Operator):
        self.operand = operand

    def evaluate(self, assign):
        return None

    def stringify(self, variables):
        return self.operand.stringify(variables)


class NegateNode(UnaryOperator):
    def __init__(self, operand: Operator):
        super().__init__(operand)

    def evaluate(self, assign):
        return not self.operand.evaluate(assign)

    def to_string(self, variables):
        return "!" + self.operand.stringify(variables)


class BinaryOperator(Operator):
    def __init__(self, lhs: Operator, rhs: Operator):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, assign):
        return None

    def stringify(self, variables):
        return f"({self.lhs.stringify(variables)} {self.rhs.stringify(variables)})"


class AndOperator(BinaryOperator):
    def __init__(self, lhs: Operator, rhs: Operator):
        super().__init__(lhs, rhs)

    def evaluate(self, assign):
        return self.lhs.evaluate(assign) and self.rhs.evaluate(assign)

    def stringify(self, variables):
        return f"({self.lhs.stringify(variables)} & {self.rhs.stringify(variables)})"


class OrOperator(BinaryOperator):
    def __init__(self, lhs: Operator, rhs: Operator):
        super().__init__(lhs, rhs)

    def evaluate(self, assign):
        return self.lhs.evaluate(assign) or self.rhs.evaluate(assign)

    def stringify(self, variables):
        return f"({self.lhs.stringify(variables)} | {self.rhs.stringify(variables)})"


class ImplicationOperator(BinaryOperator):
    def __init__(self, lhs: Operator, rhs: Operator):
        super().__init__(lhs, rhs)

    def evaluate(self, assign):
        return not self.lhs.evaluate(assign) or self.rhs.evaluate(assign)

    def stringify(self, variables):
        return f"({self.lhs.stringify(variables)} -> {self.rhs.stringify(variables)})"


class EquivalenceOperator(BinaryOperator):
    def __init__(self, lhs: Operator, rhs: Operator):
        super().__init__(lhs, rhs)

    def evaluate(self, assign):
        return not self.lhs.evaluate(assign) == self.rhs.evaluate(assign)

    def stringify(self, variables):
        return f"({self.lhs.stringify(variables)} <-> {self.rhs.stringify(variables)})"
