from enum import Enum

from logic.stream.exceptions import BadToken, FullBuffer
from logic import wordtree

whitespace = (' ', '\n', '\t')


def reverse_map(sample_dict: dict):
    """Inverte um mapa, os valores apontam para a chave."""
    reversed_map = {}
    for key, val in sample_dict.items():
        for i in val:
            reversed_map[i] = key
    return reversed_map


class Logic(Enum):
    """Elementos lógicos e parte de suas precedências"""
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
    XOR = 9
    NAND = 10
    NOR = 11


logicMap = {
    Logic.CONSTANT: ['V', 'F', 'T'],
    Logic.NOT: ['NOT', '!', '~', '¬'],
    Logic.AND: ['AND', '&', '.', '∧', '^'],
    Logic.OR: ['OR', '|', '+', '∨', 'v'],
    Logic.IMPLICATION: ['IMPLIES', '->', '→'],
    Logic.EQUIVALENCE: ['EQUAL', '<->', '⟷'],
    Logic.XOR: ['XOR', '⊻'],
    Logic.NAND: ['NAND', '↑'],
    Logic.NOR: ['NOR', '↓'],
    Logic.OPEN: ['('],
    Logic.CLOSE: [')'],
    Logic.VAR: ['p', 'q', 'r', 'A', 'B', 'C'],
}

equivalent = reverse_map(logicMap)

operators = [key for key, val in equivalent.items() if val != Logic.CONSTANT]
ignore = logicMap[Logic.CONSTANT] + logicMap[Logic.OPEN] + logicMap[Logic.CLOSE]


class ReturnString:
    def __init__(self, text=""):
        self.text = text

    def __call__(self, *args, **kwargs):
        return self.text


class Token:
    """Representa um elemento lógico dentro de uma expressão."""
    def __init__(self, kind=None, value=None):
        self.kind = kind
        self.value = value

    def __str__(self):
        return f"{type(self).__name__}(kind={self.kind}, value='{self.value}')"

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

    def match(self, expect: str):
        ch = self.source.get()
        word = str(ch)
        while expect.startswith(word):
            word += self.source.get()
        print(word)
        if word == expect:
            return True
        else:
            for c in word:
                self.source.putback(c)
            return False

    def get(self):
        if self.full:
            self.full = False
            return self.buffer

        # ch = self.source.get()
        self.index += 1

        # Compare characters
        for var in logicMap[Logic.VAR]:
            if self.match(var):
                return Token(equivalent[var], var)

        for op in sorted(operators, reverse=True):
            if self.match(op):
                return Token(equivalent[op], op)


        raise BadToken("Bad Token: char="+ self.source.get())

    def putback(self, t: Token):
        if self.full:
            raise FullBuffer("Full Buffer:", t)
        if t.kind:
            self.buffer = t
            self.full = True

    def clean(self):
        self.buffer = Token()
        self.full = False

