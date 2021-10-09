import tabulate

from core import *
from logic.stream import Logic, Token
from logic.stream.exceptions import ParseError, BadToken
from verify import setup

operator_map = {
    Logic.AND: AndOperator,
    Logic.OR: OrOperator,
    Logic.EQUIVALENCE: EquivalenceOperator,
    Logic.IMPLICATION: ImplicationOperator,
    Logic.XOR: XorOperator,
    Logic.NOR: NorOperator,
    Logic.NAND: NandOperator,
}

fbf_permitted = [Logic.OPEN, Logic.CLOSE, Logic.CONSTANT, Logic.VAR, Logic.AND, Logic.OR, Logic.NOT, Logic.EOF]


def to_operand(token: Token) -> Operand:
    """Converte Token para Operand"""
    if token.kind == Logic.CONSTANT:
        if token.value:
            return TrueOperand()
        elif not token.value:
            return FalseOperand()
    elif token.kind == Logic.VAR:
        return VarOperand(token.value)
    raise BadToken(f"{token} não é um operando.")


def to_operator(lhs: Operand, token: Token, rhs: Operand) -> Operator:
    """Construi um Operator a partir de um Token e seus Operands"""
    if token.kind in operator_map:
        return operator_map[token.kind](lhs, rhs)
    raise BadToken(f"{token} não é um operador.")


def last(tokens: list):
    """Retorna o último item sem remove-lo"""
    return tokens[-1]


def priority(token: Token):
    """Retorna a prioridade de um Token"""
    return token.kind.value


def bool_to_str(boolean: bool):
    """Converte um elemento booleano em uma string V ou F"""
    if boolean:
        return "V"
    return "F"


def generate_variables(expr_vars):
    """Gera árvore verdade a partir de varaiveis"""
    length = len(expr_vars)
    size = 2 ** length
    vars_table = [{} for _ in range(size)]
    half = size

    for var in expr_vars:
        half //= 2
        actual = True
        for j in range(1, size + 1):
            vars_table[j-1][var] = actual
            if j % half == 0:
                actual = not actual

    return vars_table


class LogicParser:
    """
    Utilizado para ser intermediario entre as entradas do úsuario e seus retornos.
    Essa classe transforma a entrada em Tokens e depois converte os Tokens em Operandos
    """
    def __init__(self):
        self.expr = None
        self.res = None
        self.operators = []
        self.operands = []
        self.valid = False

    @property
    def expr(self):
        return self._expr

    @expr.setter
    def expr(self, value):
        """Limpa os recursos quando expressão for escolhida."""
        self.valid = False
        self._expr = value
        self.operators = []
        self.operands = []

    def parse(self):
        """Função principal para conversão da entrada em Tokens e depois para Operandos"""
        setup_result: list = setup(self.expr)
        tokens: list[Token] = setup_result[0]

        expect_operand = True

        for t in tokens:
            if expect_operand:
                if t.kind in (Logic.CONSTANT, Logic.VAR):
                    self.append_operand(to_operand(t))
                    expect_operand = False
                elif t.kind == Logic.OPEN or t.kind == Logic.NOT:
                    self.operators.append(t)
                elif t.kind == Logic.EOF:
                    if len(self.operators) == 0:
                        raise ParseError("Erro de Parse")
                    elif last(self.operators).kind == Logic.OPEN:
                        raise ParseError(f"Parêntese aberto não possui fechamento {t}.")

                    raise ParseError(f"Falta operandos. {t}")
                else:
                    raise ParseError(f"Esperava variável ou constante. {t}")
            else:
                if t.kind in (Logic.AND, Logic.OR, Logic.IMPLICATION, Logic.EQUIVALENCE, Logic.XOR, Logic.NAND, Logic.NOR, Logic.EOF):
                    while True:
                        if len(self.operators) == 0:
                            break
                        if last(self.operators).kind == Logic.OPEN:
                            break

                        if priority(last(self.operators)) < priority(t):
                            break

                        operator: Token = self.operators.pop()
                        rhs: Operand = self.operands.pop()
                        lhs: Operand = self.operands.pop()

                        self.append_operand(to_operator(lhs, operator, rhs))

                    self.operators.append(t)
                    expect_operand = True
                    if t.kind == Logic.EOF:
                        break

                elif t.kind == Logic.CLOSE:
                    while True:
                        if len(self.operators) == 0:
                            raise ParseError(f"Não possui parêntese de abertura. {t}")
                        curr_op: Token = self.operators.pop()

                        if curr_op.kind == Logic.OPEN:
                            break
                        if curr_op.kind == Logic.NOT:
                            raise ParseError(f"Nenhum operando para negar. {curr_op}")

                        rhs: Operand = self.operands.pop()
                        lhs: Operand = self.operands.pop()

                        self.append_operand(to_operator(lhs, curr_op, rhs))

                    ex: Operand = self.operands.pop()
                    self.append_operand(ex)
                else:
                    raise ParseError(f"Esperando parêntese de fechada ou operador. {t}")

        assert len(self.operators) != 0
        assert self.operators.pop().kind == Logic.EOF

        if len(self.operators) != 0:
            lone_open: Token = self.operators.pop()
            assert lone_open.kind == Logic.OPEN
            raise ParseError(f"Nenhum parêntese de fechamento. {lone_open}.")

        self.valid = True
        self.res = tokens, self.operands.pop(), setup_result[1]

    def is_fbf(self):
        """Verifica se os tokens constroem uma Fórmula Bem Formada"""
        if self.res:
            for i in self.res[0]:
                if i.kind not in fbf_permitted:
                    return False
            return True
        return False

    def calculate(self):
        """Gera a tabela a partir dos resultados do parse"""
        op = self.res[1]
        v = self.res[2]
        repeat_dict = {k: k for k in v}
        truth = generate_variables(v)

        header = [k for k in sorted(v)]
        header.append(op.stringify(repeat_dict))
        table = [header]

        for var in truth:
            row = [bool_to_str(var[key]) for key in sorted(var)]
            row.append(bool_to_str(op.evaluate(var)))
            table.append(row)

        return table

    def show_table(self):
        """Usa o módulo tabulate para monstrar a tabela"""
        data = self.calculate()
        print(tabulate.tabulate(data, tablefmt='fancy_grid', stralign='center'))

    def append_operand(self, expr: Expression):
        """Adiciona um operando para os membros da classe. Enquanto o último operando é uma Negação - converte a expressão."""
        while len(self.operators) > 0 and last(self.operators).kind == Logic.NOT:
            self.operators.pop()
            expr = NotOperator(expr)

        self.operands.append(expr)
