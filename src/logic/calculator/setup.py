"""
Essa seção prepara os tokens e as variáveis de uma expressão.
"""

from logic.stream.core import ReturnString, InputStream, TokenStream, Logic, Token

text_stream = ReturnString()
cin = InputStream(text_stream)
ts = TokenStream(cin)

class SetupResult:
    def __init__(self, tokens: list[Token], variables: dict[str, bool]):
        self.tokens: list[Token] = tokens
        self.variables: dict[str, bool] = variables


def setup(expr: str) -> SetupResult:
    """Prepara uma expressão para o parse. Retorna uma lista de Tokens e um mapa com suas variáveis."""
    tokens: list[Token] = tokenize(expr)
    return SetupResult(tokens, get_vars(tokens))


def tokenize(expr: str) -> list[Token]:
    """Define a expressão na stream. A resgata com input e depois a tokeniza."""
    text_stream.text = expr
    cin.input()
    return ts.tokenize()


def get_vars(tokens: list[Token]) -> dict[str, bool]:
    """Recebe uma lista de Tokens e retorna um mapa com suas variáveis."""
    var_dict: dict[str, bool] = {}
    for v in filter(lambda x: x.kind == Logic.VAR, tokens):
        var_dict[v.value] = True
    return var_dict


def main():
    setup_result: SetupResult = setup("p | q")
    print(setup_result.tokens)
    print(setup_result.variables)


if __name__ == "__main__":
    main()
