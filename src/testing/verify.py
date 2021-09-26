from src.core.stream import ReturnString, InputStream, TokenStream, Logic

text_stream = ReturnString()
cin = InputStream(text_stream)
ts = TokenStream(cin)


def check(expr):
    tokens = check_expr(expr)
    return preliminary(tokens)


def check_expr(expr):
    text_stream.text = expr
    cin.input()
    tokens = ts.tokenize()
    return tokens


def preliminary(tokens):
    var_dict = {}
    for t in tokens:
        if t.kind == Logic.VAR:
            var_dict[t.value] = True
    return {"tokens": tokens, "var_dict": var_dict}




if __name__ == "__main__":
    check_expr("p | q adf")