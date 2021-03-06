from enum import Enum, auto

from logic.calculator.setup import setup, SetupResult
from logic.calculator.table import TruthTable

from logic.model import operators, operands, simplify
from logic.model import Expression, Operator, Operand
from logic.calculator.exceptions import ParseError

from logic.stream.core import Logic, Token, logic_map
from logic.stream.exceptions import BadToken

class ParseState(Enum):
    OPERAND = auto()
    OPERATOR = auto()
    EOF = auto()


operator_map = {
    Logic.AND: operators.AND,
    Logic.OR: operators.OR,
    Logic.EQUAL: operators.EQUAL,
    Logic.IMPLY: operators.IMPLY,
    Logic.XOR: operators.XOR,
    Logic.NOR: operators.NOR,
    Logic.NAND: operators.NAND,
}

canon_permitted: list[Logic] = [Logic.OPEN, Logic.CLOSE, Logic.CONSTANT, Logic.VAR, Logic.AND, Logic.OR, Logic.NOT, Logic.EOF]


def to_operand(token: Token) -> Operand:
    """Converte Token para Operand"""
    if token.kind == Logic.CONSTANT:
        if token.value in logic_map[Logic.TRUE]:
            return operands.TRUE()
        elif token.value in logic_map[Logic.FALSE]:
            return operands.FALSE()
    elif token.kind == Logic.VAR:
        return operands.VAR(token.value)
    raise BadToken(f"{token} não é um operando.")


def to_operator(left: Operand, token: Token, right: Operand) -> Operator:
    """Construi um Operator a partir de um Token e seus Operands"""
    if token.kind in operator_map:
        return operator_map[token.kind](left, right)
    raise BadToken(f"{token} não é um operador.")


class LogicParser:
    """
    Utilizado para ser intermediario entre as entradas do usuário e seus retornos.
    Essa classe transforma a entrada em Tokens e depois converte os Tokens em Operandos
    """

    def __init__(self, expr: str = "", *, normalize: bool = False, simplify_expression: bool = True):
        # flags
        self.normalize: bool = normalize
        self.simplify: bool = simplify_expression

        # Usado para o parse
        self.tokens: list = []
        self.state: ParseState = ParseState.OPERAND
        self.operators: list[Token] = []
        self.operands: list = []

        # Usado para calcular
        self.variables: dict[str, bool] = dict()
        self.expression: Expression = Expression()
        self.valid: bool = False

        self.expr: str = expr

    @property
    def expr(self) -> str:
        return self._expr

    @expr.setter
    def expr(self, value) -> None:
        """Limpa os recursos quando expressão for escolhida."""
        # parse
        self.tokens = []
        self.state = ParseState.OPERAND
        self._expr = value
        self.operators = []
        self.operands = []

        # calcular
        self.variables = dict()
        self.expression = Operand()
        self.valid = False

    def parse(self) -> None:
        """Função principal para conversão da entrada em Tokens e depois para Operandos"""
        if self.state == ParseState.EOF:
            return

        setup_result: SetupResult = setup(self.expr)
        tokens: list[Token] = setup_result.tokens
        # print(tokens)
        variables: dict[str, bool] = setup_result.variables

        for t in tokens:
            # Espera um operando para juntar com um operador.
            if self.state == ParseState.OPERAND:
                if t.kind in (Logic.CONSTANT, Logic.VAR):
                    self.append(to_operand(t))
                    self.state = ParseState.OPERATOR
                elif t.kind in (Logic.OPEN, Logic.NOT):
                    self.operators.append(t)
                elif t.kind == Logic.EOF:
                    if not self.operators:
                        raise ParseError("Erro de Parse")
                    elif self.last().kind == Logic.OPEN:
                        raise ParseError(f"Parêntese aberto não possui fechamento {t}.")

                    raise ParseError(f"Falta operandos. {self.last()}")
                else:
                    raise ParseError(f"Esperava variável ou constante. {t}")

            elif self.state == ParseState.OPERATOR:
                # Caso ja tenha um operando, buscar um operador
                if t.kind in (Logic.AND, Logic.OR, Logic.IMPLY, Logic.EQUAL, Logic.XOR, Logic.NAND, Logic.NOR, Logic.EOF):
                    # Se a lista de operandos estiver vazias quebrar loop, e adicionar token atual para operadores.
                    while self.operators:
                        if self.last().kind == Logic.OPEN:
                            break

                        if t.kind == Logic.IMPLY:
                            # Consequência/Conclusão aparecer primeiro à direita até a esquerda
                            if self.last().priority <= t.priority:
                                break

                        if self.last().priority < t.priority:
                            break

                        op: Token = self.operators.pop()
                        right: Operand = self.operands.pop()
                        left: Operand = self.operands.pop()
                        self.append(to_operator(left, op, right))

                        if self.operators and self.last().kind == Logic.IMPLY and op.priority > self.last().priority:
                            self.stack_all()
                            break

                    self.operators.append(t)
                    self.state = ParseState.OPERAND
                    if t.kind == Logic.EOF:
                        break

                elif t.kind == Logic.CLOSE:
                    while True:
                        if not self.operators:
                            raise ParseError(f"Não possui parêntese de abertura. {t}")
                        curr: Token = self.operators.pop()

                        if curr.kind == Logic.OPEN:
                            break
                        if curr.kind == Logic.NOT:
                            raise ParseError(f"Nenhum operando para negar. {curr}")

                        curr_right: Operand = self.operands.pop()
                        curr_left: Operand = self.operands.pop()

                        self.append(to_operator(curr_left, curr, curr_right))

                    ex: Operand = self.operands.pop()
                    self.append(ex)
                else:
                    raise ParseError(f"Esperava operador ou parêntese de fechada. {t}")

        assert self.operators
        should_eof = self.operators.pop()
        assert should_eof.kind == Logic.EOF

        if self.operators:
            lone_open: Token = self.operators.pop()
            assert lone_open.kind == Logic.OPEN
            raise ParseError(f"Nenhum parêntese de fechamento. {lone_open}.")

        self.state = ParseState.EOF
        self.valid = True
        self.tokens = tokens
        self.expression = self.operands.pop()
        self.variables = variables

        self.apply_options()

    def apply_options(self):
        """Se flag estiver ativa; aplicar modificadores."""
        if self.normalize:
            self.expression = self.expression.normalize()

        if self.simplify:
            self.expression = simplify(self.expression)
            self.variables = self.expression.variables()

    def last(self) -> Token:
        """Retorna o último operador Token sem removê-lo."""
        assert self.operators
        return self.operators[-1]

    def stack_all(self) -> None:
        """Junta todos operadores e operandos guardados."""
        while self.operators:
            op: Token = self.operators.pop()
            right: Operand = self.operands.pop()
            left: Operand = self.operands.pop()
            self.append(to_operator(left, op, right))

    def is_valid(self) -> bool:
        """Indica se não houve problemas durante o parse."""
        return self.valid

    def is_canon(self) -> bool:
        """Verifica se os tokens constroem uma Fórmula canônica."""
        for i in self.tokens:
            if i.kind not in canon_permitted:
                return False
        return True

    def get_table(self) -> TruthTable:
        """Prepara uma tabela com o operando e suas variaveis"""
        return TruthTable(self.expression, self.variables)

    def append(self, expr: Expression) -> None:
        """Adiciona um operando para os operandos da classe. Enquanto o último operando é uma Negação - converte a expressão."""
        if self.simplify:
            negates: int = 0
            while self.operators and self.last().kind == Logic.NOT:
                self.operators.pop()
                negates += 1

            if negates & 1:
                expr = operators.NOT(expr)
        else:
            while self.operators and self.last().kind == Logic.NOT:
                self.operators.pop()
                expr = operators.NOT(expr)

        self.operands.append(expr)
