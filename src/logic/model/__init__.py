"""
Essa seção representa elementos de uma expressão lógica e seus resultados.
"""

from __future__ import annotations

"""Modelos lógicos"""


class Expression:
    """Expressão que represanta ambos Operadores e Operandos."""

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    def __eq__(self, other: Expression):
        return type(self) == type(other)

    def evaluate(self, assign: dict) -> bool:
        """Calcula o resultado de forma encadeada"""
        return True

    def stringify(self, variables: dict) -> str:
        """Mostra a expressão em forma de string"""
        return "()"

    def simplify(self) -> Expression:
        """TODO: Encontrar padrões de simplificação."""
        return self

    def normalize(self):
        return self


class Operand(Expression):
    """Representa um operando."""

    def evaluate(self, assign: dict) -> bool:
        """Retorna Verdade ou Falso."""
        return True

    def stringify(self, variables: dict) -> str:
        return "()"


class Operator(Expression):
    """Representa um operador."""

    def evaluate(self, assign: dict) -> bool:
        """Realiza uma operação com base em operadores/operandos atribuidos"""
        return True

    def stringify(self, variables: dict) -> str:
        return "()"
