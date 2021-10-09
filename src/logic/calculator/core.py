"""Essa seção representa elementos de uma expressão lógica e seus resultados."""

"""Modelos lógicos"""
class Expression:
    """Expressão que represanta ambos Operadores e Operandos."""
    def __repr__(self):
        return f"{type(self).__name__}()"

    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return ""
    
    def simplify(self, assign: dict):
        return None


class Operand(Expression):
    """Representa um operando."""
    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return ""
    
    def simplify(self, assign: dict):
        return None


class Operator(Expression):
    """Representa um operador."""
    def evaluate(self, assign: dict):
        return None

    def stringify(self, variables: dict):
        return ""
    
    def simplify(self, assign: dict):
        return None


"""Constantes"""
class TrueOperand(Operand):
    """Representa uma constante Verdade."""
    def evaluate(self, assign: dict):
        return True

    def stringify(self, variables: dict):
        return "V"
    
    def simplify(self, assign: dict):
        return True


class FalseOperand(Operand):
    """Representa uma constante Falso."""
    def evaluate(self, assign: dict):
        return False

    def stringify(self, variables: dict):
        return "F"
    
    def simplify(self, assign: dict):
        return False


class VarOperand(Operand):
    """Representa uma Variável."""
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return f"{type(self).__name__}({self.var})"

    def evaluate(self, assign: dict = None):
        if assign is None:
            assign = dict()
        if self.var in assign:
            return assign[self.var]
        return True

    def stringify(self, variables: dict = None):
        if variables is None:
            assign = dict()
        if self.var in variables:
            return variables[self.var]
        return self.var
    
    def simplify(self, assign: dict):
        return assign[self.var]


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
    
    def simplify(self, assign: dict):
        return None


class NotOperator(UnaryOperator):
    """Representa um Operador unário de negação."""
    def __init__(self, operand: Expression):
        super().__init__(operand)

    def evaluate(self, assign: dict):
        return not self.operand.evaluate(assign)

    def stringify(self, variables: dict):
        return f"(¬{self.operand.stringify(variables)})"
    
    def simplify(self, assign: dict):
        return self

    def equivalences(self):
        equiv = [
            NandOperator(self.operand, self.operand),
            NorOperator(self.operand, self.operand)
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


class AndOperator(BinaryOperator):
    """Representa um Operador binário de conjunção."""
    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return self.left.evaluate(assign) and self.right.evaluate(assign)

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} ∧ {self.right.stringify(variables)})"


class OrOperator(BinaryOperator):
    """Representa um Operador binário de disjunção."""
    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return self.left.evaluate(assign) or self.right.evaluate(assign)

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} ∨ {self.right.stringify(variables)})"


class ImplicationOperator(BinaryOperator):
    """Representa um Operador binário de implicação."""
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
    """Representa um Operador binário de equivalência."""
    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return self.left.evaluate(assign) == self.right.evaluate(assign)

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} ⟷ {self.right.stringify(variables)})"

    def equivalences(self):
        equiv = [
            AndOperator(EquivalenceOperator(self.left, self.right), EquivalenceOperator(self.right, self.left)),
        ]
        return equiv


class NandOperator(BinaryOperator):
    """Representa um Operador binário de negação de conjunção."""
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


class NorOperator(BinaryOperator):
    """Representa um Operador binário de negação de disjunção."""
    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return not (self.left.evaluate(assign) or self.right.evaluate(assign))

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} ↓ {self.right.stringify(variables)})"

    def equivalences(self):
        equiv = [
            NotOperator(OrOperator(self.left, self.right)),
            AndOperator(NotOperator(self.left), NotOperator(self.right))
        ]
        return equiv


class XorOperator(BinaryOperator):
    """Representa um Operador binário de disjunção exclusiva."""
    def __init__(self, left: Expression, right: Expression):
        super().__init__(left, right)

    def evaluate(self, assign: dict):
        return not (self.left.evaluate(assign) == self.right.evaluate(assign))

    def stringify(self, variables: dict):
        return f"({self.left.stringify(variables)} ⊻ {self.right.stringify(variables)})"

    def equivalences(self):
        equiv = [
            NotOperator(EquivalenceOperator(self.left, self.right)),
            AndOperator(OrOperator(self.left, self.right), NotOperator(AndOperator(self.left, self.right)))
        ]
        return equiv


def main():
    op = ImplicationOperator(AndOperator(VarOperand('p'), VarOperand('q')), TrueOperand())
    print(op.stringify(dict(p='TESTE')))
    print(op.evaluate(dict()))


if __name__ == '__main__':
    main()
