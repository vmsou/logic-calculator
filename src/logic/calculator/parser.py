import tabulate

from logic.calculator.setup import setup, SetupResult

from logic.model import operator, operand
from logic.model import Expression, Operator, Operand
from logic.model.exceptions import ParseError

from logic.stream.core import Logic, Token, logicMap
from logic.stream.exceptions import BadToken

operator_map = {
    Logic.AND: operator.AND,
    Logic.OR: operator.OR,
    Logic.EQUIVALENCE: operator.EQUIVALENCE,
    Logic.IMPLICATION: operator.IMPLIES,
    Logic.XOR: operator.XOR,
    Logic.NOR: operator.NOR,
    Logic.NAND: operator.NAND,
}

canon_permitted: list[Logic] = [Logic.OPEN, Logic.CLOSE, Logic.CONSTANT, Logic.VAR, Logic.AND, Logic.OR, Logic.NOT, Logic.EOF]


def to_operand(token: Token) -> Operand:
    """Converte Token para Operand"""
    if token.kind == Logic.CONSTANT:
        if token.value in logicMap[Logic.TRUE]:
            return operand.TRUE()
        elif token.value in logicMap[Logic.FALSE]:
            return operand.FALSE()
    elif token.kind == Logic.VAR:
        return operand.VAR(token.value)
    raise BadToken(f"{token} não é um operando.")


def to_operator(left: Operand, token: Token, right: Operand) -> Operator:
    """Construi um Operator a partir de um Token e seus Operands"""
    if token.kind in operator_map:
        return operator_map[token.kind](left, right)
    raise BadToken(f"{token} não é um operador.")


def bool_to_str(boolean: bool) -> str:
    """Converte um elemento booleano em uma string 'V' ou 'F'"""
    if boolean:
        return "V"
    return "F"


def gen_variables(expr_vars: dict[str, bool]) -> list[dict]:
    """Gera árvore verdade a partir de variaveis"""
    variables: list = sorted(expr_vars.keys())
    length: int = len(variables)
    size: int = 2 ** length - 1
    vars_table: list[dict] = []

    for i in range(size, -1, -1):
        row: dict = {}
        b: str = format(i, f'#0{length + 2}b')[2:]  # Remove '0b'
        for c in range(0, len(b)):
            row[variables[c]] = (bool(int(b[c])))
        vars_table.append(row)
    return vars_table


class LogicParser:
    """
    Utilizado para ser intermediario entre as entradas do úsuario e seus retornos.
    Essa classe transforma a entrada em Tokens e depois converte os Tokens em Operandos
    """

    def __init__(self):
        # Usado para o parse
        self.expr: str = ""
        self.operators: list[Token] = []
        self.operands: list = []

        # Usado para calcular
        self.tokens: list = []
        self.variables: dict = dict()
        self.operand: Operand = Operand()
        self.valid: bool = False

    @property
    def expr(self) -> str:
        return self._expr

    @expr.setter
    def expr(self, value) -> None:
        """Limpa os recursos quando expressão for escolhida."""
        # parse
        self._expr = value
        self.operators = []
        self.operands = []

        # calcular
        self.tokens = []
        self.variables = dict()
        self.operand = Operand()
        self.valid = False

    def parse(self) -> None:
        """Função principal para conversão da entrada em Tokens e depois para Operandos"""
        setup_result: SetupResult = setup(self.expr)
        tokens: list[Token] = setup_result.tokens
        # print(tokens)
        variables: dict[str, bool] = setup_result.variables

        expect_operand: bool = True
        for t in tokens:
            # Espera um operando para juntar com um operador.
            if expect_operand:
                if t.kind in (Logic.CONSTANT, Logic.VAR):
                    self.append(to_operand(t))
                    expect_operand = False
                elif t.kind in (Logic.OPEN, Logic.NOT):
                    self.operators.append(t)
                elif t.kind == Logic.EOF:
                    if len(self.operators) == 0:
                        raise ParseError("Erro de Parse")
                    elif self.last().kind == Logic.OPEN:
                        raise ParseError(f"Parêntese aberto não possui fechamento {t}.")

                    raise ParseError(f"Falta operandos. {self.last()}")
                else:
                    raise ParseError(f"Esperava variável ou constante. {t}")
            else:
                # Caso ja tenha um operando, buscar um operador
                if t.kind in (Logic.AND, Logic.OR, Logic.IMPLICATION, Logic.EQUIVALENCE, Logic.XOR, Logic.NAND, Logic.NOR, Logic.EOF):
                    while True:
                        # Se a lista de operandos estiver vazias quebrar loop, e adicionar token atual para operadores.
                        if len(self.operators) == 0:
                            break
                        if self.last().kind == Logic.OPEN:
                            break

                        if t.kind == Logic.IMPLICATION:
                            # Consequência/Conclusão aparecer primeiro à direita até a esquerda
                            if self.last().priority <= t.priority:
                                break

                        if self.last().priority < t.priority:
                            break

                        op: Token = self.operators.pop()
                        right: Operand = self.operands.pop()
                        left: Operand = self.operands.pop()
                        self.append(to_operator(left, op, right))

                        if len(self.operators) and self.last().kind == Logic.IMPLICATION and op.priority > self.last().priority:
                            while True:
                                if len(self.operators) == 0:
                                    break
                                op: Token = self.operators.pop()
                                right: Operand = self.operands.pop()
                                left: Operand = self.operands.pop()

                                self.append(to_operator(left, op, right))
                            break

                    self.operators.append(t)
                    expect_operand = True
                    if t.kind == Logic.EOF:
                        break

                elif t.kind == Logic.CLOSE:
                    while True:
                        if len(self.operators) == 0:
                            raise ParseError(f"Não possui parêntese de abertura. {t}")
                        op: Token = self.operators.pop()

                        if op.kind == Logic.OPEN:
                            break
                        if op.kind == Logic.NOT:
                            raise ParseError(f"Nenhum operando para negar. {op}")

                        right: Operand = self.operands.pop()
                        left: Operand = self.operands.pop()

                        self.append(to_operator(left, op, right))

                    ex: Operand = self.operands.pop()
                    self.append(ex)
                else:
                    raise ParseError(f"Esperava operador ou parêntese de fechada. {t}")

        assert len(self.operators) != 0
        should_eof = self.operators.pop()
        assert should_eof.kind == Logic.EOF

        if len(self.operators) != 0:
            lone_open: Token = self.operators.pop()
            assert lone_open.kind == Logic.OPEN
            raise ParseError(f"Nenhum parêntese de fechamento. {lone_open}.")

        self.valid = True
        self.tokens = tokens
        self.operand = self.operands.pop()
        self.variables = variables

    def last(self) -> Token:
        """Retorna o último operador Token sem removê-lo."""
        assert len(self.operators)
        return self.operators[-1]

    def is_valid(self) -> bool:
        """Indica se não houve problemas durante o parse."""
        return self.valid

    def is_canon(self) -> bool:
        """Verifica se os tokens constroem uma Fórmula canônica."""
        for i in self.tokens:
            if i.kind not in canon_permitted:
                return False
        return True

    def calculate(self) -> tuple[list, list]:
        """Gera a tabela a partir dos resultados do parse."""
        op: Operand = self.operand
        # print(op)
        v: dict[str, bool] = self.variables
        truth: list[dict] = gen_variables(v)

        header: list[str] = [k for k in sorted(v)]
        header.append(op.stringify(dict()))
        table: list[list] = []

        for var in truth:
            row: list[str] = [bool_to_str(var[key]) for key in sorted(var)]
            row.append(bool_to_str(op.evaluate(var)))
            table.append(row)

        return header, table

    def show_table(self) -> None:
        """Usa o módulo tabulate para mostrar a tabela."""
        header, data = self.calculate()
        print(tabulate.tabulate(data, headers=header, tablefmt='fancy_grid', stralign='center'))

    def append(self, expr: Expression) -> None:
        """Adiciona um operando para os membros da classe. Enquanto o último operando é uma Negação - converte a expressão."""
        while len(self.operators) > 0 and self.last().kind == Logic.NOT:
            self.operators.pop()
            expr = operator.NOT(expr)

        self.operands.append(expr)
