from enum import Enum

from logic.stream.exceptions import BadToken, FullBuffer
from wordtree import WordTree


def reverse_map(sample_dict: dict):
    """Inverte um mapa; os valores apontam para a chave."""
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
    TRUE = 12
    FALSE = 13


"""Mapeia os Tokens com suas representações."""
logicMap = {
    Logic.TRUE: ['V', 'T'],
    Logic.FALSE: ['F'],
    Logic.CONSTANT: ['V', 'T', 'F'],
    Logic.NOT: ['NOT', 'NÃO', '!', '~', '¬'],
    Logic.AND: ['AND', 'E', '&', '.', '∧', '^'],
    Logic.OR: ['OR', 'OU', '||', '|', '+', '∨', 'v'],
    Logic.IMPLICATION: ['IMPLIES', 'IMPLICA', '->', '→'],
    Logic.EQUIVALENCE: ['EQUAL', 'IGUAL', 'EQUIVALE', '<->', '⟷', '≡', '='],
    Logic.XOR: ['XOR', '⊻', '⊕'],
    Logic.NAND: ['NAND', '↑'],
    Logic.NOR: ['NOR', '↓'],
    Logic.OPEN: ['('],
    Logic.CLOSE: [')'],
    Logic.VAR: ['p', 'q', 'r', 'A', 'B', 'C'],
}

# Utilizado para facilitiar procura
whitespace = (' ', '\n', '\t')
equivalent = reverse_map(logicMap)
operators = (key for key, val in equivalent.items() if val != Logic.CONSTANT)
word_tree = WordTree()

for char in equivalent:
    word_tree.add(char)


class ReturnString:
    """Simula um input() com texto predeterminado"""

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
    """Nesse Stream se obtem caracteres separados pelo espaço em branco."""

    def __init__(self, source=input):
        self.source = source
        self.buffer = ""

    def __bool__(self):
        return bool(self.buffer)

    def get(self):
        """Retorna um caracter."""
        return self.char_tokenize()

    def putback(self, val: str):
        """Retorna o caracter para o buffer"""
        self.buffer = val + self.buffer

    def input(self):
        """Utiliza o source para pegar um input."""
        self.buffer = self.source()

    def empty(self):
        """Verfifica se acabou o buffer."""
        return len(self.buffer) <= 0

    def char_tokenize(self):
        """Pega o primeiro caracter que não seja um espaço branco."""
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
    """Utiliza um InputStream para separar os tokens de uma string."""

    def __init__(self, source: InputStream):
        self.index = 0
        self.source = source
        self.full = False
        self.buffer = Token()

    def tokenize(self):
        """Retorna uma lista com os Tokens permitidos. Finaliza com um EOF (End-of-File)."""
        tokens = []
        ch = self.get()
        while ch.kind != "":
            tokens.append(ch)
            ch = self.get()

        tokens.append(Token(Logic.EOF))
        return tokens

    def match(self, ch: str):
        """Procura uma aproximação a partir de 1 caractere."""
        node = word_tree.root
        word = ""
        while node.has(ch):
            node = node.children[ch]
            word += ch
            ch = self.source.get()
        self.source.putback(ch)

        return word

    def get(self):
        """Retorna somente um Token permitido. Utilizando uma Arvore de Palavras para se aproximar."""
        if self.full:
            self.full = False
            return self.buffer

        ch = self.source.get()
        self.index += 1

        if ch in logicMap[Logic.CONSTANT]:
            if ch in logicMap[Logic.TRUE]:
                return Token(equivalent[ch], True)
            elif ch in logicMap[Logic.FALSE]:
                return Token(equivalent[ch], False)

        elif ch in word_tree.root.children:
            match = self.match(ch)
            if match in equivalent:
                return Token(equivalent[match], match)
            for c in match:
                self.source.putback(c)

        elif ch == "":
            return Token("", "")

        raise BadToken(f"Bad Token: char={ch}")

    def putback(self, t: Token):
        """Retorna um Token para o buffer."""
        if self.full:
            raise FullBuffer("Full Buffer:", t)
        if t.kind:
            self.buffer = t
            self.full = True

    def clean(self):
        """Limpa o buffer."""
        self.buffer = Token()
        self.full = False


def main():
    text_stream = ReturnString()
    cin = InputStream(text_stream)
    ts = TokenStream(cin)

    text_stream.text = "OU"
    print(word_tree.root.children["O"])
    cin.input()
    print(ts.match("OU"))


if __name__ == '__main__':
    main()
