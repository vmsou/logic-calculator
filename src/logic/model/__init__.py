"""
Essa seção representa elementos de uma expressão lógica e seus resultados.
"""

"""Modelos lógicos"""


class Expression:
    """Expressão que represanta ambos Operadores e Operandos."""

    def __repr__(self):
        return f"{type(self).__name__}()"

    def __str__(self):
        return self.stringify(dict())

    def evaluate(self, assign: dict):
        """Calcula o resultado de forma encadeada"""
        return None

    def stringify(self, variables: dict):
        """Mostra a expressão em forma de string"""
        return ""

    def simplify(self, assign: dict):
        """TODO: Encontrar padrões de simplificação."""
        return self


class Operand(Expression):
    """Representa um operando."""

    def evaluate(self, assign: dict):
        """Retorna Verdade ou Falso."""
        return None

    def stringify(self, variables: dict):
        return ""


class Operator(Expression):
    """Representa um operador."""

    def evaluate(self, assign: dict):
        """Realiza uma operação com base em operadores/operandos atribuidos"""
        return None

    def stringify(self, variables: dict):
        return ""