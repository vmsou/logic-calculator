from src.core.stream import ReturnString, InputStream, TokenStream, Logic

text_stream = ReturnString()
cin = InputStream(text_stream)
ts = TokenStream(cin)


def setup(expr):
    tokens = tokenize(expr)
    return get_vars(tokens)


def tokenize(expr):
    text_stream.text = expr
    cin.input()
    return ts.tokenize()


def get_vars(tokens):
    var_dict = {}
    for t in tokens:
        if t.kind == Logic.VAR:
            var_dict[t.value] = True
    return {"tokens": tokens, "vars": var_dict}


if __name__ == "__main__":
    print(setup("p | q"))