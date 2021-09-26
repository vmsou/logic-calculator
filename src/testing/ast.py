class Node:
    def evaluate(self, assign):
        return None

    def to_string(self, variables):
        return ""


class NegateNode(Node):
    def __init__(self, underlying: Node):
        self.underlying = underlying

    def evaluate(self, assign):
        return not self.underlying.evaluate(assign)

    def to_string(self, variables):
        return "!" + self.underlying.to_string(variables)


class TrueNode(Node):
    def evaluate(self, assign):
        return True

    def to_string(self, variables):
        return "V"


class FalseNode(Node):
    def evaluate(self, assign):
        return False

    def to_string(self, variables):
        return "F"


class AndNode(Node):
    def __init__(self, lhs: Node, rhs: Node):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, assign):
        return self.lhs.evaluate(assign) and self.rhs.evaluate(assign)

    def to_string(self, variables):
        return f"({self.lhs.to_string(variables)} & {self.rhs.to_string(variables)})"


class OrNode(Node):
    def __init__(self, lhs: Node, rhs: Node):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, assign):
        return self.lhs.evaluate(assign) or self.rhs.evaluate(assign)

    def to_string(self, variables):
        return f"({self.lhs.to_string(variables)} | {self.rhs.to_string(variables)})"


class ImpliesNode(Node):
    def __init__(self, lhs: Node, rhs: Node):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, assign):
        return self.lhs.evaluate(assign) or self.rhs.evaluate(assign)

    def to_string(self, variables):
        return f"({self.lhs.to_string(variables)} | {self.rhs.to_string(variables)})"