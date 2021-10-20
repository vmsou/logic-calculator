"""
Essa seção modelas os operandos, indicando seus resultados como Verdade, Falso ou uma Variável.
"""

from logic.model import Expression, Operand, ANY

"""Constantes"""
class TRUE(Operand):
    """Representa uma constante Verdade."""

    def evaluate(self, assign: dict = None) -> bool:
        """Retorna valor booleano verdade."""
        return True

    def stringify(self, variables: dict = None) -> str:
        return "V"

    def negated(self) -> Expression:
        return FALSE()


class FALSE(Operand):
    """Representa uma constante Falso."""

    def evaluate(self, assign: dict = None) -> bool:
        """Retorna valor booleano falso."""
        return False

    def stringify(self, variables: dict = None) -> str:
        return "F"

    def negated(self) -> Expression:
        return TRUE()


class VAR(Operand):
    """Representa uma Variável."""

    def __init__(self, var):
        super().__init__()
        self.var = var

    def __repr__(self):
        return f"{type(self).__name__}({self.var})"

    def __eq__(self, other):
        if type(other) == ANY:
            return True
        return super().__eq__(other) and self.var == other.var

    def evaluate(self, assign: dict = None) -> bool:
        """Durante o calculo é atribuido um valor a partir do dicionario. Caso não atribuido retorna Verdade."""
        if assign is None:
            assign = dict()
        if self.var in assign:
            return assign[self.var]
        return True

    def stringify(self, variables: dict = None) -> str:
        """Retorna em forma de string o valor atribuido no dicionario ou sua chave interna."""
        if variables is None:
            variables = dict()
        if self.var in variables:
            return variables[self.var]
        return self.var

    def variables(self):
        return {self.var: True}
