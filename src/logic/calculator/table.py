import tabulate

from logic.model import Operand


def gen_variables(expr_vars: dict[str, bool]) -> list[dict]:
    """Gera árvore verdade a partir de variaveis"""
    vars_table: list[dict] = []
    if not expr_vars:
        return vars_table
    variables: list = sorted(expr_vars.keys())
    length: int = len(variables)
    size: int = 2 ** length - 1

    for i in range(size, -1, -1):
        row: dict = {}
        b: str = format(i, f'#0{length + 2}b')[2:]  # Remove '0b'
        for c in range(0, len(b)):
            row[variables[c]] = (bool(int(b[c])))
        vars_table.append(row)
    return vars_table


def bool_to_str(boolean: bool) -> str:
    """Converte um elemento booleano em uma string 'V' ou 'F'"""
    if boolean:
        return "V"
    return "F"


class TruthTable:
    def __init__(self, operand: Operand, variables: dict[str, bool]):
        self.operand: Operand = operand
        self.variables: dict[str, bool] = variables

    def header(self) -> list[str]:
        """Constroi o cabeçalho da tabela."""
        header: list[str] = [k for k in sorted(self.variables)]
        header.append(self.operand.stringify(dict()))
        return header

    def generate(self) -> tuple[list, list]:
        """Gera a tabela verdade a partir de seu operando e variáveis."""
        truth: list[dict] = gen_variables(self.variables)
        header = self.header()
        table: list[list] = []

        for var_dict in truth:
            row: list[str] = [bool_to_str(var_dict[key]) for key in sorted(var_dict)]
            row.append(bool_to_str(self.operand.evaluate(var_dict)))
            table.append(row)

        if not truth:
            table.append([bool_to_str(self.operand.evaluate(dict()))])

        return header, table

    def show(self) -> None:
        """Prepara os dados e usa o módulo tabulate para mostrar a tabela."""
        header, data = self.generate()
        print(tabulate.tabulate(data, headers=header, tablefmt='fancy_grid', stralign='center'))
