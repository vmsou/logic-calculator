"""
Essa seção representa elementos de uma expressão lógica e seus resultados.
"""

from __future__ import annotations

"""Modelos lógicos"""


class Expression:
    """Expressão que represanta ambos Operadores e Operandos."""

    def __init__(self):
        self.type = type(self)

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    def __eq__(self, other: Expression):
        return self.type == type(other)

    def evaluate(self, assign: dict) -> bool:
        """Calcula o resultado de forma encadeada"""
        return True

    def stringify(self, variables: dict) -> str:
        """Mostra a expressão em forma de string"""
        return "()"

    def normalize(self):
        return self

    def simplify(self) -> Expression:
        """Após canônizar. Encontrar padrões de simplificações"""
        return self

    def variables(self):
        return {}


class Operand(Expression):
    """
    Representa um operando.
    Retorna Verdade/Falso ou uma variável que representa um valor booleano.
    """


class Operator(Expression):
    """
    Representa um operador.
    Realiza uma operação com base em operadores/operandos atribuidos
    """


def simplify(expr: Expression):
    old = None
    while expr != old:
        old = expr
        expr = expr.simplify()
    return expr
