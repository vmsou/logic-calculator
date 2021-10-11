"""
Essa seção modelas os operandos, indicando seus resultados como Verdade, Falso ou uma Variável.
"""

from logic.calculator.model import Operand

"""Constantes"""
class TRUE(Operand):
    """Representa uma constante Verdade."""

    def evaluate(self, assign: dict = None):
        """Retorna valor booleano verdade."""
        return True

    def stringify(self, variables: dict = None):
        return "V"


class FALSE(Operand):
    """Representa uma constante Falso."""

    def evaluate(self, assign: dict = None):
        """Retorna valor booleano falso."""
        return False

    def stringify(self, variables: dict = None):
        return "F"


class VAR(Operand):
    """Representa uma Variável."""

    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return f"{type(self).__name__}({self.var})"

    def evaluate(self, assign: dict = None):
        """Durante o calculo é atribuido um valor a partir do dicionario. Caso não atribuido retorna Verdade."""
        if assign is None:
            assign = dict()
        if self.var in assign:
            return assign[self.var]
        return True

    def stringify(self, variables: dict = None):
        """Retorna em forma de string o valor atribuido no dicionario ou sua chave interna."""
        if variables is None:
            variables = dict()
        if self.var in variables:
            return variables[self.var]
        return self.var