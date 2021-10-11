from logic.stream.core import ReturnString, InputStream, TokenStream, Logic, Token

text_stream = ReturnString()
cin = InputStream(text_stream)
ts = TokenStream(cin)


def setup(expr: str) -> tuple[list[Token], dict[str, bool]]:
    """Prepara uma expressão para o parse. Retorna uma lista de Tokens e um mapa com suas variáveis."""
    tokens: list[Token] = tokenize(expr)
    return tokens, get_vars(tokens)


def tokenize(expr: str) -> list[Token]:
    """Define a expressão na stream. A resgata com input e depois a tokeniza."""
    text_stream.text = expr
    cin.input()
    return ts.tokenize()


def get_vars(tokens: list[Token]) -> dict[str, bool]:
    var_dict: dict[str, bool] = {}
    for v in filter(lambda x: x.kind == Logic.VAR, tokens):
        var_dict[v.value] = True
    return var_dict


if __name__ == "__main__":
    print(setup("p | q"))
