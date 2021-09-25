from enum import Enum

from src.core.exceptions import BadToken, FullBuffer

whitespace = (' ', '\n')


class Logic(Enum):
    CONSTANT = 0
    NOT = 1
    AND = 2
    OR = 3
    IMPLICATION = 4,
    EQUIVALENCE = 5,
    OPEN = 6,
    CLOSE = 7,
    VAR = 8


logicMap = {
    Logic.CONSTANT: ['V', 'F'],
    Logic.NOT: ['!', '~', '¬'],
    Logic.AND: ['&', '.', '∧'],
    Logic.OR: ['|', '+', '∨', '||'],
    Logic.IMPLICATION: ['->', '→'],
    Logic.EQUIVALENCE: ['<->', '⟷'],
    Logic.OPEN: ['('],
    Logic.CLOSE: [')'],
    Logic.VAR: ['p', 'q', 'r', 's']
}

equivalent = {}

for key, val in logicMap.items():
    for i in val:
        equivalent[i] = key

operators = [key for key, val in equivalent.items() if val != Logic.CONSTANT]
ignore = logicMap[Logic.CONSTANT] + logicMap[Logic.OPEN] + logicMap[Logic.CLOSE]


class Token:
    def __init__(self, kind=None, value=None):
        self.kind = kind
        self.value = value

    def __str__(self):
        return f"{type(self).__name__}(kind='{self.kind}', value='{self.value}')"

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
        self.source = source
        self.full = False
        self.buffer = Token()

    def get(self):
        if self.full:
            self.full = False
            return self.buffer

        ch = self.source.get()

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
                while ch and ch not in ignore:
                    s += ch
                    ch = self.source.get()
                self.source.putback(ch)
                return Token(equivalent[s], s)

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



