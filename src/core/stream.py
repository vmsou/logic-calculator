from src.core.exceptions import BadToken, FullBuffer

whitespace = (' ', '\n')
operators = ('!', '&', '|', '(', ')')


class Token:
    def __init__(self, kind="", value=None):
        self.kind = kind
        self.value = value

    def __str__(self):
        return f"{type(self).__name__}(kind='{self.kind}', value='{self.value}')"

    def __repr__(self):
        return str(self)


class InputStream:
    def __init__(self, source=input):
        self.source = source
        self.line = ""

    def __bool__(self):
        return bool(self.line)

    def get(self):
        return self.char_tokenize()

    def putback(self, val):
        self.line = val + self.line

    def input(self):
        self.line = self.source()

    def empty(self):
        return len(self.line) <= 0

    def char_tokenize(self):
        index = 0
        size = len(self.line)
        value = ""
        if self.line:
            while index < size and self.line[index] in whitespace:
                index += 1
            while index < size and self.line[index] not in whitespace:
                value = self.line[index]
                self.line = self.line[index + 1:]
                return value

        return value


class TokenStream:
    def __init__(self):
        self.full = False
        self.buffer = Token()

    def get(self):
        if self.full:
            self.full = False
            return self.buffer

        ch = cin.get()

        if ch in operators:
            return Token(ch)

        elif ch == 'V':
            t = Token('c', True)
            return t

        elif ch == 'F':
            t = Token('c', False)
            return t

        elif ch == "":
            return Token()

        raise BadToken("Bad Token: char="+ch)

    def putback(self, t: Token):
        if self.full:
            raise FullBuffer("Full Buffer:", t)
        if t.kind != '':
            self.buffer = t
            self.full = True


cin = InputStream()
ts = TokenStream()
