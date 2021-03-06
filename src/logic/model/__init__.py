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
        if type(other) == ANY:
            return True
        return self.type == type(other)

    def __iter__(self):
        yield None

    def evaluate(self, assign: dict = None) -> bool:
        """Calcula o resultado de forma encadeada"""
        return True

    def stringify(self, variables: dict = None) -> str:
        """Mostra a expressão em forma de string"""
        return "()"

    def normalize(self):
        return self

    def simplify(self) -> Expression:
        """Após canônizar. Encontrar padrões de simplificações"""
        return self

    def negated(self) -> Expression:
        """Retorna forma negada da expressão."""
        return self

    def variables(self):
        """Retorna todas as varíavies em uma expressão"""
        return {}

    def equivalences(self):
        """Retorna uma lista com todas as expressões equivalentes a mesma."""
        return []


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


class ANY(Expression):
    def __eq__(self, other):
        return True


def simplify(expr: Expression):
    old = None
    while expr != old:
        old = expr
        expr = expr.simplify()
    return expr
