from enum import Enum

from src.core.exceptions import BadToken, FullBuffer

whitespace = (' ', '\n')


class Logic(Enum):
    EOF = -1
    EQUIVALENCE = 0
    IMPLICATION = 1
    OR = 2
    AND = 3
    NOT = 4
    CLOSE = 5
    OPEN = 6
    VAR = 7
    CONSTANT = 8


logicMap = {
    Logic.CONSTANT: ['V', 'F'],
    Logic.NOT: ['!', '~', '¬'],
    Logic.AND: ['&', '.', '∧'],
    Logic.OR: ['|', '+', '∨', '||'],
    Logic.IMPLICATION: ['->', '→'],
    Logic.EQUIVALENCE: ['<->', '⟷'],
    Logic.OPEN: ['('],
    Logic.CLOSE: [')'],
    Logic.VAR: ['p', 'q', 'r', 's', 'a', 'b', 'c', 'x', 'y', 'z']
}

equivalent = {}

for key, val in logicMap.items():
    for i in val:
        equivalent[i] = key

operators = [key for key, val in equivalent.items() if val != Logic.CONSTANT]
ignore = logicMap[Logic.CONSTANT] + logicMap[Logic.OPEN] + logicMap[Logic.CLOSE]


class ReturnString:
    def __init__(self, text=""):
        self.text = text

    def __call__(self, *args, **kwargs):
        return self.text


class Token:
    def __init__(self, kind=None, value=None):
        self.kind = kind
        self.value = value

    def __str__(self):
        return f"{type(self).__name__}(kind={self.kind}, value={self.value})"

    def __repr__(self):
        return str(self)


class InputStream:
    def __init__(self, source=input):
        self.source = source
        self.buffer = ""

    def __bool__(self):
        return bool(self.buffer)

    def get(self):
        return self.char_tokenize()

    def putback(self, val):
        self.buffer = val + self.buffer

    def input(self):
        self.buffer = self.source()

    def empty(self):
        return len(self.buffer) <= 0

    def char_tokenize(self):
        index = 0
        size = len(self.buffer)
        value = ""
        if self.buffer:
            while index < size and self.buffer[index] in whitespace:
                index += 1
            while index < size and self.buffer[index] not in whitespace:
                value = self.buffer[index]
                self.buffer = self.buffer[index + 1:]
                return value

        return value


class TokenStream:
    def __init__(self, source: InputStream):
        self.index = 0
        self.source = source
        self.full = False
        self.buffer = Token()

    def tokenize(self):
        tokens = []
        ch = self.get()
        while ch.kind != "":
            tokens.append(ch)
            ch = self.get()

        tokens.append(Token(Logic.EOF))
        return tokens

    def get(self):
        if self.full:
            self.full = False
            return self.buffer

        ch = self.source.get()
        self.index += 1

        # Compare characters
        if ch in operators:
            return Token(equivalent[ch], ch)

        elif ch == 'V':
            return Token(equivalent[ch], True)

        elif ch == 'F':
            return Token(equivalent[ch], False)

        elif ch == '':
            return Token("", "")

        else:
            if ch:
                s = ""
                while ch and s not in operators:
                    s += ch
                    ch = self.source.get()

                self.source.putback(ch)
                if s in equivalent:
                    return Token(equivalent[s], s)
                return Token(Logic.VAR, s)

        raise BadToken("Bad Token: char="+ch)

    def putback(self, t: Token):
        if self.full:
            raise FullBuffer("Full Buffer:", t)
        if t.kind:
            self.buffer = t
            self.full = True

    def clean(self):
        self.buffer = Token()
        self.full = False

